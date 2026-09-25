from __future__ import annotations

import os
import shutil
import subprocess


def _run(cmd: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=12, check=False)
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as exc:
        return 1, str(exc)


def lab_status() -> dict:
    code, out = _run(["iw", "phy"])
    virtual = "hwsim" in _run(["lsmod"])[1].lower()
    phys = [line.strip() for line in out.splitlines() if line.strip().startswith("Wiphy ")]
    return {"mac80211_hwsim_loaded": virtual, "phys": phys, "iw_status": code}


def create_virtual_radios(radios: int = 3) -> dict:
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    if not shutil.which("modprobe"):
        return {"ok": False, "error": "modprobe not found"}
    # mac80211_hwsim creates software-only 802.11 radios for isolated training.
    _run(["modprobe", "-r", "mac80211_hwsim"])
    code, out = _run(["modprobe", "mac80211_hwsim", f"radios={radios}"])
    status = lab_status()
    status.update({"ok": code == 0, "loader_output": out, "requested_radios": radios})
    return status


def destroy_virtual_radios() -> dict:
    if os.geteuid() != 0:
        return {"ok": False, "error": "root privileges required"}
    code, out = _run(["modprobe", "-r", "mac80211_hwsim"])
    return {"ok": code == 0, "output": out}


def lab_menu() -> dict:
    print("""
VIRTUAL WI-FI RANGE
───────────────────
This mode uses Linux mac80211_hwsim software radios.
It does not transmit RF and is intended for isolated training.

[1] Create 3 virtual radios
[2] Show lab status
[3] Destroy virtual radios
[0] Back
""")
    choice = input("lab> ").strip()
    if choice == "1":
        result = create_virtual_radios(3)
    elif choice == "2":
        result = lab_status()
    elif choice == "3":
        result = destroy_virtual_radios()
    else:
        result = {"ok": True, "action": "back"}
    print(result)
    return result
