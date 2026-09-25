from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


def _tshark(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["tshark", *args],
        capture_output=True, text=True, timeout=35, check=False
    )


def inspect_pcap(path: Path) -> dict:
    result = {
        "path": str(path),
        "exists": path.exists(),
        "eapol_frames": [],
        "handshake_visibility": "unknown",
        "notes": [],
    }
    if not path.exists():
        print("Capture file does not exist.")
        return result
    if not shutil.which("tshark"):
        result["notes"].append("tshark not installed")
        print("tshark is required for PCAP inspection.")
        return result

    p = _tshark([
        "-r", str(path),
        "-Y", "eapol",
        "-T", "fields",
        "-E", "separator=|",
        "-e", "frame.number",
        "-e", "frame.time_relative",
        "-e", "wlan.sa",
        "-e", "wlan.da",
        "-e", "eapol.type",
        "-e", "wlan_rsna_eapol.keydes.msgnr",
    ])

    frames: list[dict] = []
    for line in p.stdout.splitlines():
        cols = (line.split("|") + [""] * 6)[:6]
        frames.append({
            "frame": cols[0],
            "time": cols[1],
            "source": cols[2],
            "destination": cols[3],
            "eapol_type": cols[4],
            "message_number": cols[5],
        })
    result["eapol_frames"] = frames

    msg_nums = {f["message_number"] for f in frames if f["message_number"]}
    if {"1", "2", "3", "4"}.issubset(msg_nums):
        result["handshake_visibility"] = "complete-4-message-sequence-observed"
    elif len(frames) >= 2:
        result["handshake_visibility"] = "partial-eapol-exchange-observed"
    else:
        result["handshake_visibility"] = "no-useful-eapol-exchange-observed"

    print("\nPCAP / WPA HANDSHAKE INSPECTOR")
    print("──────────────────────────────")
    print(f"File: {path}")
    print(f"EAPOL frames: {len(frames)}")
    print(f"Handshake visibility: {result['handshake_visibility']}")
    if frames:
        print("\nFRAME   TIME       SOURCE             DESTINATION        M")
        for f in frames[:40]:
            print(
                f"{f['frame']:<7} {f['time'][:9]:<10} "
                f"{f['source']:<18} {f['destination']:<18} {f['message_number'] or '?'}"
            )
    return result
