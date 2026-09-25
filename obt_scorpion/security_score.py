from __future__ import annotations


def posture(network: dict) -> dict:
    """Return a transparent heuristic posture score from scan-visible metadata."""
    score = 100
    issues: list[str] = []
    sec = str(network.get("security", "unknown")).upper()
    pmf = str(network.get("pmf", "unknown")).lower()

    if sec == "OPEN":
        score -= 70
        issues.append("open network: no link-layer confidentiality")
    elif "WEP" in sec:
        score -= 80
        issues.append("legacy WEP detected")
    elif sec == "WPA":
        score -= 50
        issues.append("legacy WPA detected")
    elif sec == "WPA2":
        score -= 15
        issues.append("WPA2 only; evaluate WPA3 migration")
    elif "WPA2/WPA3" in sec:
        score -= 8
        issues.append("transition mode present")

    if pmf == "required":
        pass
    elif pmf == "capable":
        score -= 5
        issues.append("PMF appears optional rather than required")
    else:
        score -= 10
        issues.append("PMF requirement not visible in scan")

    if network.get("wps_hint"):
        score -= 10
        issues.append("WPS advertisement detected")

    score = max(0, min(100, score))
    if score >= 85:
        band = "strong"
    elif score >= 65:
        band = "moderate"
    else:
        band = "weak"

    return {"score": score, "band": band, "issues": issues}
