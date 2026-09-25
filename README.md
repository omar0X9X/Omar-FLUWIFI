# 🦂 OBT SCORPION — Omar-FLUWIFI

**Created by OMAR BEN TALEB**

A Kali-Linux-only wireless security operations and training platform focused on
authorized labs, defensive analysis, packet visibility, rogue/Evil-Twin
detection, WPA handshake inspection, RF reconnaissance and reproducible
virtual Wi‑Fi ranges.

> **Scope:** use only on networks you own or have explicit authorization to test.
> OBT SCORPION deliberately does not ship credential-stealing portals,
> indiscriminate deauthentication, jamming, or automated password cracking.

## Highlights

- Cinematic terminal dashboard
- Kali Linux + root + dependency pre-flight checks
- Wireless interface and monitor-capability inventory
- Live 2.4/5/6 GHz scan parsing
- Security profiling: Open/WEP/WPA/WPA2/WPA3, PMF hints, WPS hints
- Duplicate-SSID / rogue / Evil-Twin suspicion engine
- PCAP inspector with EAPOL/handshake visibility
- JSON + Markdown evidence reports
- Virtual Wi‑Fi range using `mac80211_hwsim`
- Exam-safe scope configuration
- Zero hidden network actions: every command is logged

## Install on Kali

```bash
git clone https://github.com/omar0X9X/Omar-FLUWIFI.git
cd Omar-FLUWIFI
chmod +x install.sh scorpion.py
sudo ./install.sh
sudo ./scorpion.py
```

## Main menu

```text
[1] System / adapter pre-flight
[2] Wireless reconnaissance
[3] Rogue / Evil-Twin watch
[4] PCAP + WPA handshake inspector
[5] Virtual Wi-Fi training range
[6] Generate evidence report
[7] Show scope
[0] Exit
```

## Scope configuration

Copy the example and edit it for the lab:

```bash
cp config.example.json config.json
```

The tool can restrict analysis to explicitly listed lab SSIDs/BSSIDs.

## Architecture

```text
OBT-SCORPION/
├── scorpion.py
├── install.sh
├── config.example.json
├── obt_scorpion/
│   ├── system_check.py
│   ├── wifi_scan.py
│   ├── rogue_watch.py
│   ├── pcap_analyzer.py
│   ├── lab.py
│   └── report.py
└── .github/workflows/ci.yml
```

## Why this project is different

OBT SCORPION treats every wireless incident as:

```text
DISCOVER → PROFILE → OBSERVE → DETECT → EXPLAIN → HARDEN → RETEST → REPORT
```

That makes it useful both for red/blue-team education and for demonstrating
what evidence a defender should see during a Wi‑Fi security exercise.

## License

MIT — see `LICENSE`.
