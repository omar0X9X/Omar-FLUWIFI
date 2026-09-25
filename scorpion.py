#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

from obt_scorpion.system_check import preflight
from obt_scorpion.wifi_scan import choose_interface, scan_networks, print_networks
from obt_scorpion.rogue_watch import watch_for_rogues
from obt_scorpion.pcap_analyzer import inspect_pcap
from obt_scorpion.lab import lab_menu
from obt_scorpion.report import ReportStore

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config.json"
EXAMPLE = ROOT / "config.example.json"

RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

LOGO = r"""
                         ___
                    _.-'   `-._
                 .-'  _     _  `-.
                /    (_)   (_)    \
               |        /\         |
               |   .---/  \---.    |
                \  \          /   /
                 `._\________/_.'
                    / /    \ \
               ____/ /      \ \____
              /_____/   🦂   \_____\

             O B T   S C O R P I O N
               O M A R  B E N  T A L E B
"""

def clear() -> None:
    os.system("clear")

def beep(enabled: bool) -> None:
    if enabled and sys.stdout.isatty():
        print("\a", end="", flush=True)

def load_config() -> dict:
    src = CONFIG if CONFIG.exists() else EXAMPLE
    try:
        return json.loads(src.read_text())
    except Exception:
        return {
            "owner": "OMAR BEN TALEB",
            "project": "OBT SCORPION",
            "authorized_ssids": [],
            "authorized_bssids": [],
            "report_dir": "reports",
            "sound": True,
            "cinematic": True,
        }

def boot(cfg: dict) -> None:
    clear()
    print(CYAN + LOGO + RESET)
    stages = [
        "KALI CORE",
        "RF ENGINE",
        "PACKET INSPECTOR",
        "ROGUE DETECTOR",
        "EVIDENCE VAULT",
        "SCOPE GUARD",
    ]
    cinematic = bool(cfg.get("cinematic", True))
    for stage in stages:
        print(f"  {DIM}INITIALIZING{RESET} {stage:<22}", end="", flush=True)
        if cinematic:
            time.sleep(0.12)
        print(GREEN + " ONLINE" + RESET)
    beep(bool(cfg.get("sound", True)))
    if cinematic:
        time.sleep(0.25)

def menu() -> None:
    print(f"""
{BOLD}{CYAN}COMMAND CENTER{RESET}
  [1] System / adapter pre-flight
  [2] Wireless reconnaissance
  [3] Rogue / Evil-Twin watch
  [4] PCAP + WPA handshake inspector
  [5] Virtual Wi-Fi training range
  [6] Generate evidence report
  [7] Show authorized scope
  [0] Exit
""")

def show_scope(cfg: dict) -> None:
    print(f"Owner: {cfg.get('owner','OMAR BEN TALEB')}")
    print("Authorized SSIDs:")
    for s in cfg.get("authorized_ssids", []):
        print(f"  - {s}")
    print("Authorized BSSIDs:")
    for b in cfg.get("authorized_bssids", []):
        print(f"  - {b}")
    if not cfg.get("authorized_ssids") and not cfg.get("authorized_bssids"):
        print("  (No explicit targets configured; passive inspection only.)")

def main() -> int:
    cfg = load_config()
    report = ReportStore(ROOT / cfg.get("report_dir", "reports"))
    boot(cfg)

    while True:
        menu()
        choice = input(f"{CYAN}scorpion>{RESET} ").strip()

        if choice == "1":
            result = preflight(verbose=True)
            report.add("preflight", result)
        elif choice == "2":
            iface = choose_interface()
            if iface:
                nets = scan_networks(iface)
                print_networks(nets)
                report.add("wireless_scan", {"interface": iface, "networks": nets})
        elif choice == "3":
            iface = choose_interface()
            if iface:
                events = watch_for_rogues(
                    iface,
                    authorized_ssids=set(cfg.get("authorized_ssids", [])),
                    seconds=30,
                )
                report.add("rogue_watch", {"interface": iface, "events": events})
        elif choice == "4":
            p = input("PCAP/CAP path: ").strip()
            result = inspect_pcap(Path(p))
            report.add("pcap_analysis", result)
        elif choice == "5":
            result = lab_menu()
            report.add("virtual_lab", result)
        elif choice == "6":
            md, js = report.write()
            print(f"{GREEN}Report written:{RESET}\n  {md}\n  {js}")
        elif choice == "7":
            show_scope(cfg)
        elif choice == "0":
            print("SCORPION OFFLINE")
            return 0
        else:
            print(RED + "Unknown command." + RESET)

        input("\nPress Enter to return to command center...")
        clear()
        print(CYAN + LOGO + RESET)

if __name__ == "__main__":
    raise SystemExit(main())
