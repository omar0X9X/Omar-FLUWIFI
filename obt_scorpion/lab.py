from __future__ import annotations

import os
import shutil
import signal
import subprocess
from pathlib import Path

LAB_DIR = Path("/tmp/obt-scorpion-range")


def _run(cmd: list[str], timeout: int = 12) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
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


def hwsim_interfaces() -> list[str]:
    # Critical safety property: the training arena only accepts software radios.
    return [i for i in _all_interfaces() if _driver_name(i) == "mac80211_hwsim"]


def lab_status() -> dict:
    code, out = _run(["iw", "phy"])
    loaded = "mac80211_hwsim" in _run(["lsmod"])[1]
    phys = [line.strip() for line in out.splitlines() if line.strip().startswith("Wiphy ")]
    return {
        "mac80211_hwsim_loaded": loaded,
        "phys": phys,
        "hwsim_interfaces": hwsim_interfaces(),
        "iw_status": code,
        "twin_running": any((LAB_DIR / name).exists() for name in ("ap1.pid", "ap2.pid")),
    }


def stop_twin_demo() -> dict:
    stopped: list[int] = []
    errors: list[str] = []
    for name in ("ap1.pid", "ap2.pid"):
        p = LAB_DIR / name
        if not p.exists():
            continue
        try:
            pid = int(p.read_text().strip())
            os.kill(pid, signal.SIGTERM)
            stopped.append(pid)
        except ProcessLookupError:
            pass
        except Exception as exc:
            errors.append(f"{name}: {exc}")
        finally:
            try:
                p.unlink()
            except FileNotFoundError:
                pass
    return {"ok": not errors, "stopped_pids": stopped, "errors": errors}


def create_virtual_radios(radios: int = 3) -> dict:
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    if not shutil.which("modprobe"):
        return {"ok": False, "error": "modprobe not found"}

    stop_twin_demo()
    _run(["modprobe", "-r", "mac80211_hwsim"])
    code, out = _run(["modprobe", "mac80211_hwsim", f"radios={radios}"])
    status = lab_status()
    status.update({"ok": code == 0, "loader_output": out, "requested_radios": radios})
    return status


def _hostapd_config(iface: str, ssid: str, channel: int) -> str:
    return f"""interface={iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
auth_algs=1
wpa=0
ignore_broadcast_ssid=0
logger_stdout=-1
logger_stdout_level=2
"""


def start_twin_demo(ssid: str = "OBT_LAB") -> dict:
    """Start two same-SSID APs strictly on mac80211_hwsim software radios."""
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    if not shutil.which("hostapd"):
        return {"ok": False, "error": "hostapd not installed"}

    ifaces = hwsim_interfaces()
    if len(ifaces) < 3:
        created = create_virtual_radios(3)
        if not created.get("ok"):
            return created
        ifaces = hwsim_interfaces()

    if len(ifaces) < 3:
        return {"ok": False, "error": "could not obtain 3 mac80211_hwsim radios"}

    # Refuse physical adapters even if interface discovery changes.
    ap1, ap2, observer = ifaces[:3]
    if any(_driver_name(i) != "mac80211_hwsim" for i in (ap1, ap2, observer)):
        return {"ok": False, "error": "safety check failed: non-hwsim interface detected"}

    stop_twin_demo()
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    cfg1 = LAB_DIR / "ap1.conf"
    cfg2 = LAB_DIR / "ap2.conf"
    cfg1.write_text(_hostapd_config(ap1, ssid, 1))
    cfg2.write_text(_hostapd_config(ap2, ssid, 6))

    for iface in (ap1, ap2, observer):
        _run(["ip", "link", "set", iface, "down"])
        _run(["iw", "dev", iface, "set", "type", "managed"])
        _run(["ip", "link", "set", iface, "up"])

    c1, o1 = _run(["hostapd", "-B", "-P", str(LAB_DIR / "ap1.pid"), str(cfg1)])
    c2, o2 = _run(["hostapd", "-B", "-P", str(LAB_DIR / "ap2.pid"), str(cfg2)])

    ok = c1 == 0 and c2 == 0
    if not ok:
        stop_twin_demo()

    return {
        "ok": ok,
        "mode": "software-radio-only",
        "ssid": ssid,
        "legitimate_lab_ap": {"interface": ap1, "channel": 1},
        "twin_lab_ap": {"interface": ap2, "channel": 6},
        "observer": observer,
        "hostapd_output": [o1, o2],
        "note": "Both APs exist only inside mac80211_hwsim; no physical RF transmission.",
    }


def destroy_virtual_radios() -> dict:
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    stopped = stop_twin_demo()
    code, out = _run(["modprobe", "-r", "mac80211_hwsim"])
    return {"ok": code == 0, "output": out, "twin_stop": stopped}


def lab_menu() -> dict:
    print("""
VIRTUAL WI-FI RANGE
───────────────────
Linux mac80211_hwsim software radios only.
No physical RF transmission is used by this arena.

[1] Create 3 virtual radios
[2] Start same-SSID Evil-Twin detection arena
[3] Show lab status
[4] Stop twin arena
[5] Destroy virtual radios
[0] Back
""")
    choice = input("lab> ").strip()
    if choice == "1":
        result = create_virtual_radios(3)
    elif choice == "2":
        ssid = input("Lab SSID [OBT_LAB]: ").strip() or "OBT_LAB"
        result = start_twin_demo(ssid)
    elif choice == "3":
        result = lab_status()
    elif choice == "4":
        result = stop_twin_demo()
    elif choice == "5":
        result = destroy_virtual_radios()
    else:
        result = {"ok": True, "action": "back"}

    print(result)
    return result
