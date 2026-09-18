"""Seeded SonarQube Vulnerabilities example. DEMO ONLY - never run or deploy this code.

The functions below are intentionally exploitable. They are defined but
never called from main.py, so no HTTP endpoint can reach them; the file
exists purely as a static-analysis target.

Seeded flaws:
- run_diagnostic: OS command injection from unsanitized input (S2076)
- lookup_user:    SQL injection via string concatenation (S3649)
- hash_password:  weak MD5 hashing for passwords (S4790)
"""
import hashlib
import os
import sqlite3
import sys


def run_diagnostic():
    """VULNERABILITY: command injection (rule S2076).

    sys.argv is user-controlled input. Concatenating it into an
    os.system call lets an attacker append arbitrary shell commands,
    for example "localhost; rm -rf /". Pass an argument list to
    subprocess with shell=False instead.
    """
    target = sys.argv[1]
    os.system("ping -c 1 " + target)


def lookup_user():
    """VULNERABILITY: SQL injection (rule S3649).

    The query is built by concatenating an environment variable, a
    user-controlled taint source, directly into SQL. A value like
    ' OR '1'='1 returns every row. Use parameterized queries instead.
    """
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
    """VULNERABILITY: weak password hashing (rule S4790).

    MD5 is fast and unsalted, so password hashes can be brute forced or
    rainbow-tabled. Use a slow, salted password hash such as bcrypt,
    scrypt, or argon2. SonarQube reports this rule as a security
    finding; in current analyzer versions it surfaces as a Security
    Hotspot, which is itself a useful classification talking point.
    """
    return hashlib.md5(password.encode()).hexdigest()
