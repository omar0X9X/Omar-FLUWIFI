# OBT SCORPION — Exam Demo Runbook

## 1. Launch

```bash
sudo scorpion
```

Show the startup banner and run **System / adapter pre-flight** first.

## 2. RF reconnaissance

Choose the lab Wi-Fi interface and run **Wireless reconnaissance**.

Explain the visible fields:

- SSID / BSSID
- RSSI signal
- channel
- WPA generation
- PMF visibility
- WPS hint
- heuristic posture score

## 3. Evil-Twin detection arena

Open **Virtual Wi-Fi training range** and:

1. Create 3 virtual radios.
2. Start the same-SSID twin arena.
3. Use the observer software radio to scan.
4. Run **Rogue / Evil-Twin watch**.

The arena creates two software-only access points with the same SSID on
different channels. The detector should flag the duplicate identity and
fingerprint mismatch.

The lab engine contains a hard safety check: it refuses to use a radio unless
its kernel driver is `mac80211_hwsim`.

## 4. PCAP / handshake demonstration

Choose **PCAP + WPA handshake inspector** and provide an instructor-approved
capture. Show the EAPOL frame timeline and whether a full 4-message sequence
is visible.

## 5. Evidence

Run **Generate evidence report**.

Show both output formats:

- Markdown: human-readable
- JSON: machine-readable

## 6. Closing explanation

Use the model:

```text
DISCOVER → PROFILE → OBSERVE → DETECT → EXPLAIN → HARDEN → RETEST → REPORT
```

This demonstrates both wireless protocol knowledge and engineering discipline.
