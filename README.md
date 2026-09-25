# 🦂 OBT SCORPION — Omar-FLUWIFI

**Created by OMAR BEN TALEB**

A Kali-Linux-only wireless security operations and training platform for
authorized labs. It combines RF reconnaissance, Rogue/Evil-Twin detection,
a reproducible software-radio attack/defense range, WPA handshake analysis,
security-posture scoring and evidence reporting.

> Use only on networks you own or have explicit authorization to test.
> Active training actions are hard-bound to Linux mac80211_hwsim software
> radios. They reject physical Wi-Fi adapters.

## Current capabilities

### Recon / defense

- Cinematic terminal command center
- Kali Linux / root / dependency pre-flight
- Wireless interface inventory
- Live 2.4 / 5 / 6 GHz reconnaissance
- WPA/WPA2/WPA3, PMF and WPS visibility
- Heuristic 0–100 wireless posture score with reasons
- Duplicate-SSID / Rogue / Evil-Twin suspicion engine
- PCAP + EAPOL / 4-way-handshake timeline inspector
- Markdown + JSON evidence reports

### Active Kali training range

The active range uses four mac80211_hwsim radios:

~~~text
 WPA2 ORIGINAL AP          OPEN SAME-SSID TWIN
       channel 1                channel 6
           \                      /
            \                    /
              OBSERVER RADIO
                    |
              VIRTUAL CLIENT
~~~

Working lab actions:

- real hostapd WPA2 original access point
- real hostapd same-SSID twin access point
- DHCP service on the twin
- wildcard DNS redirection to the training portal
- captive portal served on 10.77.0.1
- portal event logging without storing submitted tokens
- real 802.11 deauthentication frames inside hwsim only
- virtual WPA2 client using wpa_supplicant
- live EAPOL capture with TShark
- automatic M1/M2/M3/M4 inspection
- single-candidate PSK validation only against the SCORPION-generated hwsim capture
- service teardown and virtual-radio cleanup

The captive portal deliberately requests a **training token**, not a real
password, and does not store the submitted token.

## Install on Kali

~~~bash
git clone https://github.com/omar0X9X/Omar-FLUWIFI.git
cd Omar-FLUWIFI
chmod +x install.sh scorpion.py
sudo ./install.sh
sudo scorpion
~~~

The installer adds iw, tshark, aircrack-ng, hostapd, wpa_supplicant,
dnsmasq, python3-scapy and required networking/kernel tools.

## Command center

~~~text
[1] System / adapter pre-flight
[2] Wireless reconnaissance
[3] Rogue / Evil-Twin watch
[4] PCAP + WPA handshake inspector
[5] Virtual Wi-Fi training range
[6] Generate evidence report
[7] Show authorized scope
[0] Exit
~~~

Inside option **5**:

~~~text
[1] Create 4 virtual radios
[2] Start WPA2 original + same-SSID Twin Arena
[3] Start DHCP + DNS redirect + Captive Portal
[4] Send lab-only deauth burst
[5] Capture WPA2 4-way handshake in the lab
[6] Validate one PSK candidate against SCORPION lab capture
[7] Show lab status
[8] Show portal training events
[9] Stop lab services
[10] Destroy virtual radios
~~~

## Safety boundary

Every active wireless training action checks that selected interfaces use
the kernel driver mac80211_hwsim. The deauthentication engine also checks
that its target BSSID belongs to the SCORPION-generated lab state.

The PSK validation module only accepts the capture at:

~~~text
/tmp/obt-scorpion-range/handshake.pcap
~~~

when that capture was registered by the SCORPION hwsim handshake workflow.

## Suggested exam sequence

~~~text
PRE-FLIGHT
   ↓
CREATE HWSIM RANGE
   ↓
WPA2 ORIGINAL + SAME-SSID TWIN
   ↓
DHCP + DNS + CAPTIVE PORTAL
   ↓
LAB DEAUTH TEST
   ↓
VIRTUAL CLIENT WPA2 CONNECTION
   ↓
LIVE 4-WAY HANDSHAKE CAPTURE
   ↓
M1 / M2 / M3 / M4 ANALYSIS
   ↓
SINGLE-CANDIDATE LAB VALIDATION
   ↓
ROGUE / EVIL-TWIN DETECTION
   ↓
EVIDENCE REPORT
~~~

## Project layout

~~~text
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
│   ├── portal_server.py
│   ├── lab.py
│   └── report.py
├── tests/
│   └── test_core.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── EXAM_DEMO.md
└── .github/workflows/ci.yml
~~~

## Design model

~~~text
DISCOVER → PROFILE → EMULATE → OBSERVE → DETECT → EXPLAIN → HARDEN → RETEST → REPORT
~~~

See docs/EXAM_DEMO.md for the presentation runbook.

## License

MIT — see LICENSE.
