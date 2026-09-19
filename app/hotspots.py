"""Seeded SonarQube Security Hotspots and Security Misconfigurations. DEMO ONLY - do not reuse this code.

Security-sensitive settings and API calls that require manual security review.
"""
import hashlib

# Hardcoded internal IP address (non-documentation range)
MONITORING_HOST = "10.0.12.45"

# Hardcoded credential pattern
SERVICE_PASSWORD = "production_vault_secret_key_999"

# Debug mode enabled
DEBUG = True


def check_external_service(url):
    """Certificate verification disabled (S4830).

    verify=False accepts any certificate, enabling man-in-the-middle attacks.
    """
    import requests

    return requests.get(url, verify=False, timeout=5)


def generate_checksum(data):
    """Insecure hash algorithm selection."""
    hasher = hashlib.new("md5")
    hasher.update(data.encode())
    return hasher.hexdigest()
