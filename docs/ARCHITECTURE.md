# Architecture

OBT SCORPION is split into small engines so each capability can be tested and
replaced independently.

```text
                     ┌─────────────────────┐
                     │   scorpion.py UI    │
                     └──────────┬──────────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
     ┌───────▼───────┐  ┌───────▼────────┐ ┌──────▼───────┐
     │  RF Scanner   │  │ Rogue Detector │ │ PCAP Inspector│
     └───────┬───────┘  └───────┬────────┘ └──────┬───────┘
             │                  │                  │
             └──────────────────┼──────────────────┘
                                │
                         ┌──────▼──────┐
                         │ ReportStore │
                         └─────────────┘

     ┌───────────────────────────────────────────────┐
     │ Virtual Range: mac80211_hwsim-only radios    │
     │ original AP  <-> twin AP <-> observer radio  │
     └───────────────────────────────────────────────┘
```

## Trust boundaries

- Passive RF discovery can enumerate nearby beacons.
- The virtual Twin Arena is hard-bound to `mac80211_hwsim`.
- No credential collection is implemented.
- No physical-radio deauthentication or jamming engine is implemented.
- PCAP analysis is offline and does not alter networks.

## Evidence model

All major actions return structured dictionaries. The command center stores
these events and can export Markdown and JSON reports.
