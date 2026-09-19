"""Seeded SonarQube Vulnerabilities example. DEMO ONLY - never run or deploy this code.

The functions below are intentionally exploitable. They are defined but
never called from main.py, so no HTTP endpoint can reach them; the file
exists purely as a static-analysis target.
"""
import hashlib
import os
import random
import sqlite3
import sys

# VULNERABILITY (S2068): hardcoded credentials
DB_PASSWORD = "SuperAdminPassword123!"
PASSWORD = "hardcoded_master_secret"

# VULNERABILITY (S5332): clear-text protocol
REMOTE_FTP_BACKUP = "ftp://backup.internal.company.com:21/db_dump.sql"


def run_diagnostic():
    """VULNERABILITY (S2076): command injection from unsanitized input."""
    target = sys.argv[1]
    os.system("ping -c 1 " + target)


def lookup_user():
    """VULNERABILITY (S3649): SQL injection via string concatenation."""
    username = os.environ.get("DEMO_USERNAME", "admin")
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    connection = sqlite3.connect("demo.db")
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()


def hash_password(password):
    """VULNERABILITY (S4790): weak MD5 password hashing."""
    return hashlib.md5(password.encode()).hexdigest()


def hash_legacy_token(token):
    """VULNERABILITY (S4790): weak SHA-1 token hashing."""
    return hashlib.sha1(token.encode()).hexdigest()


def generate_session_token():
    """VULNERABILITY (S2245): pseudo-random number generator used in security context.

    random is not cryptographically secure and should not be used to generate tokens.
    """
    token = f"{random.random()}-{random.randint(100000, 999999)}"
    return token


def make_world_writable(file_path):
    """VULNERABILITY (S2612): file permissions set to world-accessible."""
    os.chmod(file_path, 0o777)
