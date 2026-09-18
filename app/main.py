"""SonarLens demo application entry point.

SonarLens is a deliberately flawed demo: a small Flask task manager whose
source tree is seeded with one representative example of each SonarQube
issue category, one category per file:

    bugs.py             Bugs
    vulnerabilities.py  Vulnerabilities
    hotspots.py         Security Hotspots
    smells.py           Code Smells
    duplication.py      Duplications

Everything in those files is demo-only and intentionally defective. The
HTTP endpoints below only call get_item from bugs.py (whose off-by-one
is part of the demo); none of the seeded vulnerable functions are ever
invoked, so nothing here is externally exploitable.

Run with: python app/main.py  (or: cd app && python main.py)
"""
from flask import Flask, jsonify, request

import bugs
import duplication
import hotspots
import smells
import vulnerabilities

# Importing every seed module keeps the demo one coherent, runnable
# program. The manifest below documents that wiring; nothing in it is
# executed beyond the import itself.
SEED_MODULES = {
    "bugs": bugs,
    "vulnerabilities": vulnerabilities,
    "hotspots": hotspots,
    "smells": smells,
    "duplication": duplication,
}

app = Flask(__name__)

# In-memory task store. The app exists to host seeded issues, not to
# manage real data, so persistence is intentionally absent.
TASKS = []


@app.get("/health")
def health():
    """Liveness check. Also exposes the seeded debug flag from hotspots.py."""
    return jsonify({"status": "ok", "debug": hotspots.DEBUG})


@app.get("/tasks")
def list_tasks():
    """Return every task currently held in memory."""
    return jsonify(TASKS)


@app.post("/tasks")
def add_task():
    """Add a task. Body: JSON with a non-empty "title" field."""
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    if not title:
        return jsonify({"error": "a non-empty 'title' field is required"}), 400
    TASKS.append(title)
    return jsonify({"index": len(TASKS) - 1, "title": title}), 201


@app.get("/tasks/<int:idx>")
def get_task(idx):
    """Return one task by index.

    Uses the seeded get_item from bugs.py. Its off-by-one guard lets
    idx == len(TASKS) through, which raises IndexError and surfaces as
    an HTTP 500. That failure is intentional and is part of the demo.
    """
    return jsonify({"index": idx, "title": bugs.get_item(TASKS, idx)})


if __name__ == "__main__":
    # debug comes from hotspots.py: the seeded "debug flag left enabled"
    # hotspot. Localhost only; never expose this app beyond the machine.
    app.run(host="127.0.0.1", port=5000, debug=hotspots.DEBUG)
