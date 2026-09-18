"""Seeded SonarQube Security Hotspots example. DEMO ONLY - do not reuse this code.

Hotspots are code SonarQube flags for manual review because whether they
are actually dangerous depends on context. None of these settings are
read by anything security-relevant; main.py only reads DEBUG for the
/health endpoint and the dev-server flag.

Seeded hotspots:
- MONITORING_HOST:        hardcoded IP address (S1313)
- SECRET_KEY:             hardcoded credential (S2068)
- DEBUG:                  debug mode left enabled
- check_external_service: TLS certificate verification disabled (S4830)
"""

# SECURITY HOTSPOT (S1313): hardcoded IP addresses are security-sensitive.
# A reviewer must confirm this host is intentional and not an internal
# endpoint leaking infrastructure details. The address is from the
# TEST-NET-3 documentation range, so it routes nowhere.
MONITORING_HOST = "203.0.113.42"

# SECURITY HOTSPOT (S2068): hardcoded credentials are security-sensitive.
# Secrets belong in environment variables or a secret manager, not source.
SECRET_KEY = "lens-demo-signing-secret"

# SECURITY HOTSPOT: a debug flag left enabled ships verbose internals to
# end users if this configuration reaches a deployed environment.
DEBUG = True


def check_external_service(url):
    """SECURITY HOTSPOT (S4830): certificate verification disabled.

    verify=False accepts any certificate, enabling man-in-the-middle
    attacks. A reviewer must confirm the target really warrants it, for
    example a pinned internal test endpoint. requests is imported
    lazily so the app runs without the package installed.
    """
    import requests

    return requests.get(url, verify=False, timeout=5)
