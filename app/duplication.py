"""Seeded SonarQube Duplications example. DEMO ONLY - do not reuse this code.

The functions below contain large, duplicated blocks of code exceeding SonarQube's
Copy-Paste-Detection (CPD) threshold (10+ lines and 100+ tokens).
"""


def validate_customer_account_a(account_data):
    """First version of full customer account validation pipeline."""
    if not isinstance(account_data, dict):
        return {"valid": False, "error": "Account payload must be a dictionary object"}

    username = str(account_data.get("username", "")).strip()
    if len(username) < 3 or len(username) > 30:
        return {"valid": False, "error": "Username length must be between 3 and 30 characters"}

    email = str(account_data.get("email", "")).strip().lower()
    if not email or "@" not in email or "." not in email:
        return {"valid": False, "error": "Invalid email address format provided"}

    age = account_data.get("age")
    if not isinstance(age, int) or age < 18 or age > 120:
        return {"valid": False, "error": "Account holder age must be an integer between 18 and 120"}

    postal_code = str(account_data.get("postal_code", "")).strip()
    if not postal_code or not postal_code.isalnum() or len(postal_code) > 10:
        return {"valid": False, "error": "Postal code must be non-empty alphanumeric up to 10 characters"}

    allowed_roles = ["VIEWER", "EDITOR", "ADMINISTRATOR", "AUDITOR"]
    role = str(account_data.get("role", "")).upper().strip()
    if role not in allowed_roles:
        return {"valid": False, "error": f"Role must be one of the supported tiers: {allowed_roles}"}

    status = str(account_data.get("status", "ACTIVE")).upper().strip()
    if status not in ["ACTIVE", "PENDING_VERIFICATION", "SUSPENDED"]:
        return {"valid": False, "error": "Account status flag is unrecognized"}

    return {
        "valid": True,
        "normalized_username": username,
        "normalized_email": email,
        "assigned_role": role,
        "status": status,
    }


def validate_customer_account_b(account_data):
    """Second copy of full customer account validation pipeline - duplicate of A."""
    if not isinstance(account_data, dict):
        return {"valid": False, "error": "Account payload must be a dictionary object"}

    username = str(account_data.get("username", "")).strip()
    if len(username) < 3 or len(username) > 30:
        return {"valid": False, "error": "Username length must be between 3 and 30 characters"}

    email = str(account_data.get("email", "")).strip().lower()
    if not email or "@" not in email or "." not in email:
        return {"valid": False, "error": "Invalid email address format provided"}

    age = account_data.get("age")
    if not isinstance(age, int) or age < 18 or age > 120:
        return {"valid": False, "error": "Account holder age must be an integer between 18 and 120"}

    postal_code = str(account_data.get("postal_code", "")).strip()
    if not postal_code or not postal_code.isalnum() or len(postal_code) > 10:
        return {"valid": False, "error": "Postal code must be non-empty alphanumeric up to 10 characters"}

    allowed_roles = ["VIEWER", "EDITOR", "ADMINISTRATOR", "AUDITOR"]
    role = str(account_data.get("role", "")).upper().strip()
    if role not in allowed_roles:
        return {"valid": False, "error": f"Role must be one of the supported tiers: {allowed_roles}"}

    status = str(account_data.get("status", "ACTIVE")).upper().strip()
    if status not in ["ACTIVE", "PENDING_VERIFICATION", "SUSPENDED"]:
        return {"valid": False, "error": "Account status flag is unrecognized"}

    return {
        "valid": True,
        "normalized_username": username,
        "normalized_email": email,
        "assigned_role": role,
        "status": status,
    }
