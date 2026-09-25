from __future__ import annotations

import time
from collections import defaultdict

from .wifi_scan import scan_networks


def _fingerprint(n: dict) -> tuple:
    return (
        n.get("security"),
        n.get("pmf"),
        n.get("channel"),
        (n.get("bssid") or "")[:8],
    )


def analyze_snapshot(networks: list[dict], authorized_ssids: set[str]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for n in networks:
        grouped[n.get("ssid", "<hidden>")].append(n)

    events: list[dict] = []
    for ssid, aps in grouped.items():
        if ssid == "<hidden>" or len(aps) < 2:
            continue
        fps = {_fingerprint(ap) for ap in aps}
        severity = "medium"
        reasons = ["same SSID advertised by multiple BSSIDs"]
        if len(fps) > 1:
            severity = "high"
            reasons.append("security/channel/vendor-prefix fingerprint mismatch")
        if authorized_ssids and ssid not in authorized_ssids:
            reasons.append("SSID outside configured lab scope")
        events.append({
            "type": "duplicate_ssid",
            "ssid": ssid,
            "severity": severity,
            "reasons": reasons,
            "access_points": aps,
        })
    return events


def watch_for_rogues(iface: str, authorized_ssids: set[str], seconds: int = 30) -> list[dict]:
    print(f"\nSCORPION WATCH — {seconds}s")
    print("Looking for duplicate SSIDs and fingerprint changes. Ctrl-C stops early.\n")
    deadline = time.time() + seconds
    all_events: list[dict] = []
    seen: set[tuple] = set()

    try:
        while time.time() < deadline:
            nets = scan_networks(iface)
            for ev in analyze_snapshot(nets, authorized_ssids):
                key = (ev["ssid"], ev["severity"], tuple(sorted(a["bssid"] for a in ev["access_points"])))
                if key in seen:
                    continue
                seen.add(key)
                all_events.append(ev)
                print(f"⚠ {ev['severity'].upper():<6} SSID={ev['ssid']}  APs={len(ev['access_points'])}")
                for reason in ev["reasons"]:
                    print(f"    - {reason}")
            time.sleep(3)
    except KeyboardInterrupt:
        pass

    if not all_events:
        print("No duplicate-SSID anomalies observed in this window.")
    return all_events
