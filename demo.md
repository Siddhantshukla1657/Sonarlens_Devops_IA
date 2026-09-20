# SonarLens — Demo Guide

> **⚠️ Teaching project only.**  
> All unsafe code in `app/` is intentional and seeded for SonarQube to detect.  
> Do not reuse or deploy any of it in a real system.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Clone and Configure](#2-clone-and-configure)
3. [Start the SonarQube Server](#3-start-the-sonarqube-server)
4. [Create the Project and Token](#4-create-the-project-and-token)
5. [Run the Scan](#5-run-the-scan)
6. [Walk the Dashboard](#6-walk-the-dashboard)
7. [Run the Flask Demo App (Optional)](#7-run-the-flask-demo-app-optional)
8. [Teardown](#8-teardown)
9. [Troubleshooting](#9-troubleshooting)
10. [Presenter Checklist](#10-presenter-checklist)

---

## 1. Prerequisites

| Requirement | Notes |
|---|---|
| **Docker Desktop** | Must be running before any `docker` commands |
| **Docker Compose** | Bundled with Docker Desktop on Windows and macOS |
| **Python 3.12+** | Only needed for [Step 7](#7-run-the-flask-demo-app-optional) |
| **Git** | To clone the repo |
| **A browser** | To view the SonarQube dashboard |

> **Linux note:** You may need to raise the kernel map count for SonarQube to start:
> ```bash
> sudo sysctl -w vm.max_map_count=262144
> ```

---

## 2. Clone and Configure

```bash
git clone https://github.com/Siddhantshukla1657/sonarlens.git
cd sonarlens
```

Copy the environment template and fill in your local values:

```bash
cp .env.example .env
```

Open `.env` and set at minimum:

```dotenv
POSTGRES_HOST=postgres
POSTGRES_USER=sonar
POSTGRES_PASSWORD=change-this-local-password
POSTGRES_DB=sonar

# Set these after creating a project token in Step 4
SONAR_HOST_URL=http://host.docker.internal:9000
SONAR_TOKEN=replace-with-your-sonarqube-token
```

> `.env` is Git-ignored. Never commit it.

---

## 3. Start the SonarQube Server

```bash
docker compose up -d
```

This starts two containers:

| Container | Purpose | Port |
|---|---|---|
| `sonarlens-sonarqube` | SonarQube Community Edition web UI + analysis engine | `9000` |
| `sonarlens-postgres` | Backing PostgreSQL 17 database | internal |

**Check container health:**

```bash
docker compose ps
```

**Follow startup logs** (first boot can take 60–90 seconds):

```bash
docker compose logs -f sonarqube
```

The server is ready when you see:

```
SonarQube is operational
```

Then open: **http://localhost:9000**

---

## 4. Create the Project and Token

1. Open **http://localhost:9000** in a browser.
2. Log in with `admin` / `admin`.
3. **Change the default password** when prompted (required even for local demos).
4. Go to **Projects → Add project → Manually**.
5. Set the values exactly as shown:

   | Field | Value |
   |---|---|
   | Project display name | `SonarLens` |
   | Project key | `sonarlens` |

   > The project key **must** be `sonarlens` — it matches `sonar-project.properties`.

6. Click **Set up → Generate a token**.
7. Give the token a name (e.g., `demo-token`) and click **Generate**.
8. **Copy the token immediately** — it is shown only once.
9. Paste the token into `.env`:

   ```dotenv
   SONAR_TOKEN=<paste-token-here>
   ```

---

## 5. Run the Scan

Choose the script for your OS:

**Linux / macOS / Git Bash (WSL)**
```bash
./run-scan.sh
```

**Windows — Command Prompt**
```cmd
run-scan.bat
```

**Windows — PowerShell**
```powershell
.\run-scan.ps1
```

All three scripts read `SONAR_HOST_URL` and `SONAR_TOKEN` from `.env` and launch the official `sonarsource/sonar-scanner-cli` Docker container, mounting the current directory read-only.

### What the scanner does

```
1. Reads sonar-project.properties  →  projectKey=sonarlens, sources=app/
2. Analyzes all Python files under app/
3. POSTs the analysis report to SONAR_HOST_URL
4. Prints EXECUTION SUCCESS on completion
```

### SONAR_HOST_URL quick reference

| Environment | Value |
|---|---|
| Docker Desktop (Windows / macOS) | `http://host.docker.internal:9000` |
| Linux — Docker bridge | `http://172.17.0.1:9000` |
| Linux — scanner on compose network | `http://sonarlens-sonarqube:9000` |

A **successful run** ends with:

```
INFO: EXECUTION SUCCESS
INFO: Total time: ...
```

A **failed run** (bad token or server unreachable) fails fast with a clear error message and leaves the dashboard unchanged.

---

## 6. Walk the Dashboard

Open the project dashboard:

**http://localhost:9000/dashboard?id=sonarlens**

### Issue seed map

| Seed file | SonarQube category | What to show |
|---|---|---|
| `app/bugs.py` | **Bugs** | Division by zero (`average_score`), off-by-one guard (`get_item`), possible `None` dereference (`print_value`), ignored `sorted()` return value (`normalize_titles`) |
| `app/vulnerabilities.py` | **Vulnerabilities** | OS command injection (`run_diagnostic`), SQL string concat (`lookup_user`), weak MD5 hashing (`hash_password`) |
| `app/hotspots.py` | **Security Hotspots** | Hardcoded IP (`MONITORING_HOST`), hardcoded credential (`SECRET_KEY`), debug flag left on (`DEBUG = True`), TLS cert check disabled (`verify=False`) |
| `app/smells.py` | **Code Smells** | 8-parameter function (`generate_report`), 4-level nesting (`classify_reading`), dead store (`audit_task`), oversized class (`TaskScribe`) |
| `app/duplication.py` | **Duplications** | Two near-identical email validators (`validate_email_a`, `validate_email_b`) exceeding the CPD token threshold |

### Suggested walkthrough order

1. **Overview tab** — Show total finding counts across all categories.
2. **Bugs** — Open `app/bugs.py`. Point at `get_item` (the off-by-one) as a live, reproducible crash (demonstrated in Step 7).
3. **Vulnerabilities** — Open `app/vulnerabilities.py`. Show `run_diagnostic` where `sys.argv` is concatenated into `os.system`.
4. **Security Hotspots** — Open `app/hotspots.py`. Show the hardcoded `SECRET_KEY` and the `verify=False` line.
5. **Code Smells** — Open `app/smells.py`. Show the 8-parameter function signature.
6. **Duplications** — Open `app/duplication.py`. Show the two functions and the highlighted duplicated block.

> **Tip:** Clicking a finding in the SonarQube UI links directly to the offending line. Use this to transition between the dashboard and source view.

---

## 7. Run the Flask Demo App (Optional)

The Flask app is the target the scanner analyzes. Running it is optional — the scan reads source files and does not require the app to be running. Start it to demonstrate the live bug.

### Setup

**Linux / macOS / Git Bash:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
cd app && python main.py
```

**Windows — PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r app\requirements.txt
python app\main.py
```

The app starts at **http://127.0.0.1:5000**.

### Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Landing page |
| `GET` | `/health` | Liveness check (also reports the debug flag) |
| `GET` | `/tasks` | List all tasks |
| `POST` | `/tasks` | Add a task — body: `{"title": "..."}` |
| `GET` | `/tasks/<idx>` | Get one task by zero-based index |

### Demonstrate the live bug

**Step 1 — Add a task:**

```bash
curl -X POST http://127.0.0.1:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Review SonarQube findings"}'
```

**Step 2 — Fetch at valid index 0 (succeeds):**

```bash
curl http://127.0.0.1:5000/tasks/0
```

**Step 3 — Fetch at index 1 (triggers the off-by-one bug → HTTP 500):**

```bash
curl -i http://127.0.0.1:5000/tasks/1
```

Expected output:

```
HTTP/1.1 500 INTERNAL SERVER ERROR
...
IndexError: list index out of range
```

This is the `get_item` off-by-one from `app/bugs.py` surfacing as a real crash. Map it back to the SonarQube Bugs finding.

**Windows — PowerShell equivalents:**

```powershell
# Add a task
Invoke-RestMethod -Uri http://127.0.0.1:5000/tasks -Method Post `
  -ContentType "application/json" -Body '{"title":"Review SonarQube findings"}'

# Fetch valid task
Invoke-WebRequest http://127.0.0.1:5000/tasks/0

# Trigger the bug
Invoke-WebRequest http://127.0.0.1:5000/tasks/1
```

---

## 8. Teardown

Stop the Flask app with `Ctrl+C` in its terminal.

Stop Docker services:

```bash
docker compose down
```

To also remove all stored SonarQube and Postgres data (volumes):

```bash
docker compose down -v
```

> Omit `-v` if you want to preserve the SonarQube project and scan history for another demo session.

---

## 9. Troubleshooting

| Symptom | Fix |
|---|---|
| SonarQube never starts | Run `docker compose logs sonarqube`. On Linux, raise `vm.max_map_count` to `262144`. |
| `EXECUTION FAILURE` — auth error | Token is wrong or expired. Regenerate in SonarQube → **My Account → Security → Tokens** and update `.env`. |
| `EXECUTION FAILURE` — connection refused | Scanner cannot reach the SonarQube container. Verify `SONAR_HOST_URL` using the table in [Step 5](#5-run-the-scan). |
| Zero findings in a category | Confirm the scan ended with `EXECUTION SUCCESS` and that `sonar.sources=app` in `sonar-project.properties` was not overridden. Re-run the scan. |
| Flask app port already in use | Kill the process on port 5000, or set `PORT=5001` before starting: `PORT=5001 python app/main.py` |
| `docker compose` not found | Use `docker-compose` (with hyphen) for older Docker Engine versions. |

---

## 10. Presenter Checklist

Use this before a live demo:

- [ ] Docker Desktop is running.
- [ ] `.env` exists with a valid `POSTGRES_PASSWORD` and `SONAR_TOKEN`.
- [ ] `docker compose up -d` completed without errors.
- [ ] `docker compose ps` shows both containers as **Up**.
- [ ] SonarQube is accessible at **http://localhost:9000** (login page loads).
- [ ] Project key `sonarlens` exists in SonarQube.
- [ ] Scan script (`run-scan.sh` / `.bat` / `.ps1`) ends with `EXECUTION SUCCESS`.
- [ ] Dashboard at **http://localhost:9000/dashboard?id=sonarlens** shows findings in all five categories.
- [ ] (Optional) Flask app starts and `/health` returns 200.
- [ ] Browser tabs pre-opened: dashboard overview, each category tab.

---

*Licensed under the [MIT License](LICENSE).*
