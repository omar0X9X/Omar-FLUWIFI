import unittest

from obt_scorpion.lab import _hostapd_config
from obt_scorpion.portal_server import PAGE
from obt_scorpion.rogue_watch import analyze_snapshot
from obt_scorpion.security_score import posture


class SecurityScoreTests(unittest.TestCase):
    def test_open_network_scores_lower_than_wpa3(self):
        open_net = {"security": "OPEN", "pmf": "unknown", "wps_hint": False}
        wpa3 = {"security": "WPA3-SAE", "pmf": "required", "wps_hint": False}
        self.assertLess(posture(open_net)["score"], posture(wpa3)["score"])

    def test_wps_reduces_score(self):
        base = {"security": "WPA2", "pmf": "capable", "wps_hint": False}
        wps = dict(base)
        wps["wps_hint"] = True
        self.assertLess(posture(wps)["score"], posture(base)["score"])


class RogueWatchTests(unittest.TestCase):
    def test_duplicate_ssid_with_mismatch_is_high(self):
        nets = [
            {
                "ssid": "OBT_LAB",
                "bssid": "02:00:00:00:00:01",
                "security": "WPA2",
                "pmf": "required",
                "channel": 1,
            },
            {
                "ssid": "OBT_LAB",
                "bssid": "06:11:22:33:44:55",
                "security": "OPEN",
                "pmf": "unknown",
                "channel": 6,
            },
        ]
        events = analyze_snapshot(nets, {"OBT_LAB"})
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["severity"], "high")

    def test_single_ap_has_no_duplicate_event(self):
        nets = [
            {
                "ssid": "OBT_LAB",
                "bssid": "02:00:00:00:00:01",
                "security": "WPA3-SAE",
                "pmf": "required",
                "channel": 36,
            }
        ]
        self.assertEqual(analyze_snapshot(nets, {"OBT_LAB"}), [])


class LabConfigTests(unittest.TestCase):
    def test_wpa2_original_configuration(self):
        conf = _hostapd_config("wlan0", "OBT_LAB", 1, "ScorpionLab2026!")
        self.assertIn("wpa=2", conf)
        self.assertIn("wpa_key_mgmt=WPA-PSK", conf)
        self.assertIn("rsn_pairwise=CCMP", conf)

    def test_twin_configuration_is_open_for_training_portal(self):
        conf = _hostapd_config("wlan1", "OBT_LAB", 6, None)
        self.assertIn("wpa=0", conf)


class PortalSafetyTests(unittest.TestCase):
    def test_portal_explicitly_warns_against_real_passwords(self):
        self.assertIn("Do not enter a real password", PAGE)

    def test_portal_uses_training_token_not_password_field(self):
        self.assertIn('name="token"', PAGE)
        self.assertNotIn('name="password"', PAGE)


if __name__ == "__main__":
    unittest.main()
