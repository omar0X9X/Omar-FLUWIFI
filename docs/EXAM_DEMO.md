# OBT SCORPION — Exam Demo Runbook

## 1. Launch

Run:

    sudo scorpion

Start with **System / adapter pre-flight** and show that Kali, root privileges,
TShark, Aircrack-ng, hostapd, wpa_supplicant, dnsmasq and Scapy are ready.

## 2. Passive RF reconnaissance

Use **Wireless reconnaissance** on the instructor-authorized physical adapter.

Explain SSID/BSSID, RSSI, channel, WPA generation, PMF, WPS and posture score.
Passive discovery is separate from the active range.

## 3. Build the isolated active range

Open **Virtual Wi-Fi training range**:

1. Create 4 virtual radios.
2. Start the Twin Arena:
   - WPA2 original AP on channel 1
   - open same-SSID twin AP on channel 6
   - observer radio
   - virtual client radio

Show the state output and BSSIDs.

## 4. Start the captive stack

Select **Start DHCP + DNS redirect + Captive Portal**.

Explain:

- twin gateway: 10.77.0.1
- DHCP leases: 10.77.0.20-10.77.0.100
- wildcard DNS points to 10.77.0.1
- portal runs on port 80
- portal accepts only a synthetic training token
- the submitted token is never stored

## 5. Management-frame resilience demo

Choose the lab-only deauth action.

Before frame transmission, the engine verifies that the transmitter is
mac80211_hwsim and the AP BSSID belongs to the SCORPION-generated lab state.

## 6. Generate a real WPA2 handshake

Choose **Capture WPA2 4-way handshake in the lab**.

SCORPION switches the observer to monitor mode, tunes it to channel 1, starts
TShark, connects the virtual WPA2 client through wpa_supplicant, records EAPOL,
and reports M1/M2/M3/M4 visibility.

Capture path:

    /tmp/obt-scorpion-range/handshake.pcap

## 7. Candidate validation

Choose **Validate one PSK candidate against SCORPION lab capture**.

This accepts one candidate only and refuses arbitrary external captures.
Demonstrate one wrong synthetic candidate and the configured lab PSK.

## 8. Rogue / Twin detection

Demonstrate the same-SSID mismatch:

    SSID: same
    BSSID: different
    channel: different
    security: WPA2 vs OPEN

Explain why this produces a high-suspicion event.

## 9. Evidence

Generate Markdown and JSON reports.

## 10. Closing model

    DISCOVER
       ↓
    PROFILE
       ↓
    EMULATE
       ↓
    OBSERVE
       ↓
    DETECT
       ↓
    EXPLAIN
       ↓
    HARDEN
       ↓
    RETEST
       ↓
    REPORT

The active training chain is repeatable while being technically unable to
select a physical Wi-Fi radio.
