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
from flask import Flask, jsonify, request, Response

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


@app.get("/")
def index():
    """Root landing page listing all available endpoints and seeded issue files."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SonarLens Demo App</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:system-ui,sans-serif;background:#0f1117;color:#e2e8f0;min-height:100vh;padding:40px 24px}
    h1{font-size:2rem;font-weight:700;color:#60a5fa;margin-bottom:6px}
    .subtitle{color:#94a3b8;margin-bottom:36px;font-size:.95rem}
    .card{background:#1e2330;border:1px solid #2d3748;border-radius:12px;padding:24px;margin-bottom:20px}
    .card h2{font-size:1rem;font-weight:600;color:#f8fafc;margin-bottom:14px;letter-spacing:.05em;text-transform:uppercase;font-size:.8rem;color:#94a3b8}
    table{width:100%;border-collapse:collapse}
    td,th{padding:9px 12px;text-align:left;border-bottom:1px solid #2d3748;font-size:.9rem}
    th{color:#94a3b8;font-weight:500;font-size:.8rem;text-transform:uppercase}
    tr:last-child td{border-bottom:none}
    .method{font-weight:700;font-size:.78rem;padding:2px 8px;border-radius:4px;display:inline-block}
    .get{background:#1e3a5f;color:#60a5fa}
    .post{background:#1a3a2a;color:#4ade80}
    a{color:#60a5fa;text-decoration:none}
    a:hover{text-decoration:underline}
    .tag{background:#312e5e;color:#a78bfa;font-size:.75rem;padding:2px 8px;border-radius:4px;margin-left:4px}
    .badge{display:inline-block;font-size:.75rem;padding:2px 8px;border-radius:4px;font-weight:600}
    .bug{background:#3b1f1f;color:#f87171}
    .vuln{background:#3b2a1f;color:#fb923c}
    .hot{background:#3b361f;color:#fbbf24}
    .smell{background:#1f3b2a;color:#4ade80}
    .dup{background:#1f2a3b;color:#60a5fa}
  </style>
</head>
<body>
  <h1>&#128269; SonarLens</h1>
  <p class="subtitle">Deliberately flawed Flask demo &mdash; one SonarQube issue category per file</p>

  <div class="card">
    <h2>HTTP Endpoints</h2>
    <table>
      <tr><th>Method</th><th>Path</th><th>Description</th></tr>
      <tr><td><span class="method get">GET</span></td><td><a href="/">/</a></td><td>This page</td></tr>
      <tr><td><span class="method get">GET</span></td><td><a href="/health">/health</a></td><td>Liveness check &amp; debug flag state</td></tr>
      <tr><td><span class="method get">GET</span></td><td><a href="/tasks">/tasks</a></td><td>List all in-memory tasks</td></tr>
      <tr><td><span class="method post">POST</span></td><td>/tasks</td><td>Add a task &mdash; JSON body <code>{"title":"..."}</code></td></tr>
      <tr><td><span class="method get">GET</span></td><td>/tasks/&lt;idx&gt;</td><td>Get task by index (off-by-one bug is live here)</td></tr>
    </table>
  </div>

  <div class="card">
    <h2>Seeded SonarQube Issue Categories</h2>
    <table>
      <tr><th>File</th><th>Category</th><th>Key Rules</th></tr>
      <tr><td><code>app/bugs.py</code></td><td><span class="badge bug">Bugs</span></td><td>S3518, S2259, S2201, S1763, S1656, S1143</td></tr>
      <tr><td><code>app/vulnerabilities.py</code></td><td><span class="badge vuln">Vulnerabilities</span></td><td>S4790, S2068, S2245, S2612, S5332, SQL/OS injection</td></tr>
      <tr><td><code>app/hotspots.py</code></td><td><span class="badge hot">Security Hotspots</span></td><td>S1313, S2068, S4507, S4830</td></tr>
      <tr><td><code>app/smells.py</code></td><td><span class="badge smell">Code Smells</span></td><td>S107, S1066, S1854, S1481, S1172, S1135, S1134, S1144</td></tr>
      <tr><td><code>app/duplication.py</code></td><td><span class="badge dup">Duplications</span></td><td>CPD 100+ token threshold</td></tr>
    </table>
  </div>

  <div class="card">
    <h2>Quick Demo</h2>
    <table>
      <tr><th>What</th><th>Command</th></tr>
      <tr><td>Add a task</td><td><code>curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d "{\"title\":\"demo\"}"</code></td></tr>
      <tr><td>Trigger the off-by-one bug</td><td><code>curl http://127.0.0.1:5000/tasks/1</code> &nbsp;(when only 1 task exists &rarr; HTTP 500)</td></tr>
    </table>
  </div>
</body>
</html>"""
    return Response(html, mimetype="text/html")


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
