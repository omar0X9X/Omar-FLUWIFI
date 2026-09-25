# 🦂 OBT SCORPION — Omar-FLUWIFI

**Created by OMAR BEN TALEB**

A Kali-Linux-only wireless security operations and training platform for
authorized labs: RF reconnaissance, rogue/Evil-Twin detection, WPA handshake
inspection, security-posture scoring, evidence reporting and a reproducible
software-radio Wi-Fi range.

> Use only on networks you own or have explicit authorization to test.
> The public build does not contain credential-stealing portals,
> indiscriminate deauthentication, RF jamming or automated password cracking.

## What is working

- Cinematic terminal command center
- Kali Linux / root / dependency pre-flight
- Wireless interface inventory
- Live 2.4 / 5 / 6 GHz reconnaissance
- WPA/WPA2/WPA3, PMF and WPS visibility
- Heuristic 0–100 wireless posture score with reasons
- Duplicate-SSID / Rogue / Evil-Twin suspicion engine
- PCAP + EAPOL / 4-way-handshake timeline inspector
- Markdown + JSON evidence reports
- `mac80211_hwsim` virtual Wi-Fi range
- **Same-SSID Twin Arena:** two real software AP processes on separate virtual radios
- Hard safety property: Twin Arena refuses non-hwsim radios
- GitHub Actions compile/import/unit-test CI

## Install on Kali

```bash
git clone https://github.com/omar0X9X/Omar-FLUWIFI.git
cd Omar-FLUWIFI
chmod +x install.sh scorpion.py
sudo ./install.sh
sudo scorpion
```

## Command center

```text
[1] System / adapter pre-flight
[2] Wireless reconnaissance
[3] Rogue / Evil-Twin watch
[4] PCAP + WPA handshake inspector
[5] Virtual Wi-Fi training range
[6] Generate evidence report
[7] Show authorized scope
[0] Exit
```

## Twin Arena

Inside option **5**, OBT SCORPION can load three Linux
`mac80211_hwsim` radios and run two hostapd instances advertising the same
lab SSID on separate channels. A third software radio acts as observer.

```text
 ORIGINAL LAB AP         TWIN LAB AP
      ch 1                  ch 6
        \                    /
         \                  /
           same SSID identity
                 |
           OBSERVER RADIO
                 |
         SCORPION DETECTOR
```

No physical RF adapter is accepted by this arena.

## Handshake inspector

Give SCORPION an instructor-approved `.pcap` or `.cap` capture. It uses
TShark to display EAPOL frames, endpoints, relative timing and message numbers
where available, then classifies the visible exchange as complete, partial or
not useful.

## Scope configuration

```bash
cp config.example.json config.json
```

Edit the allowed lab SSIDs/BSSIDs before the assessment.

## Project layout

```text
Omar-FLUWIFI/
├── scorpion.py
├── install.sh
├── config.example.json
├── obt_scorpion/
│   ├── system_check.py
│   ├── wifi_scan.py
│   ├── security_score.py
│   ├── rogue_watch.py
│   ├── pcap_analyzer.py
│   ├── lab.py
│   └── report.py
├── tests/
│   └── test_core.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── EXAM_DEMO.md
└── .github/workflows/ci.yml
```

## Design model

```text
DISCOVER → PROFILE → OBSERVE → DETECT → EXPLAIN → HARDEN → RETEST → REPORT
```

See `docs/EXAM_DEMO.md` for a short presentation sequence.

## License

MIT — see `LICENSE`.
