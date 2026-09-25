from __future__ import annotations

import importlib.util
import os
import platform
import shutil
import subprocess
from pathlib import Path


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, timeout=8, check=False
        ).stdout.strip()
    except Exception:
        return ""


def is_kali() -> bool:
    os_release = Path("/etc/os-release")
    if not os_release.exists():
        return False
    text = os_release.read_text(errors="ignore").lower()
    return "kali" in text


def interfaces() -> list[dict]:
    out = _run(["iw", "dev"])
    found: list[dict] = []
    current: dict | None = None
    for raw in out.splitlines():
        line = raw.strip()
        if line.startswith("Interface "):
            if current:
                found.append(current)
            current = {"name": line.split(maxsplit=1)[1]}
        elif current and line.startswith("type "):
            current["type"] = line.split(maxsplit=1)[1]
        elif current and line.startswith("addr "):
            current["mac"] = line.split(maxsplit=1)[1]
        elif current and line.startswith("channel "):
            parts = line.split()
            current["channel"] = parts[1] if len(parts) > 1 else "?"
    if current:
        found.append(current)
    return found


def preflight(verbose: bool = False) -> dict:
    commands = [
        "iw",
        "ip",
        "tshark",
        "aircrack-ng",
        "hostapd",
        "wpa_supplicant",
        "wpa_cli",
        "dnsmasq",
        "modprobe",
    ]
    result = {
        "kali": is_kali(),
        "root": os.geteuid() == 0,
        "kernel": platform.release(),
        "commands": {name: bool(shutil.which(name)) for name in commands},
        "python_modules": {
            "scapy": importlib.util.find_spec("scapy") is not None,
        },
        "interfaces": interfaces(),
    }
    result["ready"] = (
        result["kali"]
        and result["root"]
        and all(result["commands"].values())
        and all(result["python_modules"].values())
    )

    if verbose:
        print("\nPRE-FLIGHT SECURITY CHECK")
        print("─────────────────────────")
        print(f"Kali Linux          {'✓' if result['kali'] else '✕'}")
        print(f"Root privileges     {'✓' if result['root'] else '✕'}")
        for name, ok in result["commands"].items():
            print(f"{name:<20}{'✓' if ok else '✕'}")
        for name, ok in result["python_modules"].items():
            print(f"python:{name:<13}{'✓' if ok else '✕'}")
        print(f"\nRange readiness     {'READY' if result['ready'] else 'CHECK FAILED ITEMS'}")
        print("\nWireless interfaces:")
        if result["interfaces"]:
            for i in result["interfaces"]:
                print(f"  {i.get('name')}  type={i.get('type','?')}  mac={i.get('mac','?')}")
        else:
            print("  none detected")
    return result
