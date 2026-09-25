from __future__ import annotations

import re
import subprocess

from .security_score import posture
from .system_check import interfaces


def choose_interface() -> str | None:
    ints = interfaces()
    if not ints:
        print("No wireless interfaces detected.")
        return None
    print("Wireless interfaces:")
    for idx, item in enumerate(ints, 1):
        print(f"  [{idx}] {item.get('name')} ({item.get('type','?')})")
    raw = input("Select interface: ").strip()
    try:
        pos = int(raw) - 1
        if 0 <= pos < len(ints):
            return str(ints[pos]["name"])
    except Exception:
        pass
    print("Invalid interface.")
    return None


def _security(block: str) -> str:
    upper = block.upper()
    has_rsn = "RSN:" in upper
    has_wpa = "WPA:" in upper
    if "SAE" in upper:
        return "WPA3-SAE" if not has_wpa else "WPA2/WPA3"
    if has_rsn:
        return "WPA2"
    if has_wpa:
        return "WPA"
    if "PRIVACY" in upper:
        return "WEP/legacy"
    return "OPEN"


def _pmf(block: str) -> str:
    upper = block.upper()
    if "MFP REQUIRED" in upper or "MFPR" in upper:
        return "required"
    if "MFP CAPABLE" in upper or "MFPC" in upper:
        return "capable"
    return "unknown"


def _freq_to_channel(freq: int | None) -> int | None:
    if freq is None:
        return None
    if freq == 2484:
        return 14
    if 2412 <= freq <= 2472:
        return (freq - 2407) // 5
    if 5000 <= freq <= 5895:
        return (freq - 5000) // 5
    if 5955 <= freq <= 7115:
        return (freq - 5950) // 5
    return None


def scan_networks(iface: str) -> list[dict]:
    try:
        p = subprocess.run(
            ["iw", "dev", iface, "scan"],
            capture_output=True, text=True, timeout=25, check=False
        )
    except Exception as exc:
        print(f"Scan failed: {exc}")
        return []
    if p.returncode != 0:
        print(p.stderr.strip() or "Scan failed.")
        return []

    chunks = re.split(r"(?=^BSS\s)", p.stdout, flags=re.MULTILINE)
    rows: list[dict] = []
    for block in chunks:
        m_bss = re.search(r"^BSS\s+([0-9a-fA-F:]{17})", block, re.MULTILINE)
        if not m_bss:
            continue
        m_ssid = re.search(r"^\s*SSID:\s*(.*)$", block, re.MULTILINE)
        m_sig = re.search(r"^\s*signal:\s*([-\d.]+)\s*dBm", block, re.MULTILINE)
        m_freq = re.search(r"^\s*freq:\s*(\d+)", block, re.MULTILINE)
        m_chan = re.search(r"DS Parameter set: channel (\d+)", block)
        ssid = (m_ssid.group(1).strip() if m_ssid else "<hidden>") or "<hidden>"
        freq = int(m_freq.group(1)) if m_freq else None
        row = {
            "ssid": ssid,
            "bssid": m_bss.group(1).lower(),
            "signal_dbm": float(m_sig.group(1)) if m_sig else None,
            "frequency_mhz": freq,
            "channel": int(m_chan.group(1)) if m_chan else _freq_to_channel(freq),
            "security": _security(block),
            "pmf": _pmf(block),
            "wps_hint": "WPS:" in block.upper(),
        }
        row["posture"] = posture(row)
        rows.append(row)

    rows.sort(
        key=lambda x: x["signal_dbm"] if x["signal_dbm"] is not None else -999,
        reverse=True,
    )
    return rows


def print_networks(networks: list[dict]) -> None:
    if not networks:
        print("No networks found.")
        return
    print("\nWIRELESS RECONNAISSANCE")
    print("─" * 116)
    print(
        f"{'SSID':<26} {'BSSID':<18} {'SIG':>6} {'CH':>4} "
        f"{'SECURITY':<14} {'PMF':<9} {'WPS':<4} {'SCORE':>5}"
    )
    print("─" * 116)
    for n in networks:
        sig = "?" if n["signal_dbm"] is None else f"{n['signal_dbm']:.0f}"
        ch = "?" if n["channel"] is None else str(n["channel"])
        score = n.get("posture", {}).get("score", "?")
        print(
            f"{n['ssid'][:25]:<26} {n['bssid']:<18} {sig:>6} {ch:>4} "
            f"{n['security']:<14} {n['pmf']:<9} "
            f"{'yes' if n['wps_hint'] else 'no':<4} {str(score):>5}"
        )
