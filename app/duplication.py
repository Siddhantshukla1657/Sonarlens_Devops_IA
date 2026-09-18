"""Seeded SonarQube Duplications example. DEMO ONLY - do not reuse this code.

The two functions below are deliberately near-identical so SonarQube's
duplication detector (token-based, default threshold 10 tokens) flags
the shared block. Renaming variables would not hide it, because
duplication is measured on tokens, not names.

Both validate a form email field: length cap, required @, and a
required dot in the domain part. In real code this would be one
shared function.
"""
MAX_EMAIL_LENGTH = 254


def validate_email_a(address):
    """First copy of the validation logic, version A."""
    if address is None:
        return False
    if len(address) > MAX_EMAIL_LENGTH:
        return False
    if "@" not in address:
        return False
    local_part, domain_part = address.rsplit("@", 1)
    if not local_part or not domain_part:
        return False
    if "." not in domain_part:
        return False
    return True


def validate_email_b(address):
    """Second copy of the validation logic, version B: identical except for names."""
    if address is None:
        return False
    if len(address) > MAX_EMAIL_LENGTH:
        return False
    if "@" not in address:
        return False
    local_part, domain_part = address.rsplit("@", 1)
    if not local_part or not domain_part:
        return False
    if "." not in domain_part:
        return False
    return True
