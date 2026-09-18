# SonarLens — Todo

> Last updated: 2026-09-18. Check items off as they're completed; keep this file in sync with actual progress.

## Phase 1: Seeded demo application
- [x] Set up project structure (`app/` directory, `requirements.txt` with Flask)
- [x] Write `main.py` with `/health`, `/tasks` (GET, POST), `/tasks/<idx>` (GET)
- [x] Write `bugs.py`
  - [x] Division with no zero-check
  - [x] Off-by-one bug in `get_item`
  - [x] Possible null dereference in a value-printing helper
  - [x] Ignored return value of `sorted()` (extra bug seed)
- [x] Write `vulnerabilities.py`
  - [x] Command injection via unsanitized shell call
  - [x] Weak password hashing (MD5)
  - [x] SQL query built through string concatenation
- [x] Write `hotspots.py`
  - [x] Disabled TLS certificate verification
  - [x] Debug flag left enabled
  - [x] Hardcoded secret key
  - [x] Hardcoded IP address (extra hotspot seed)
- [x] Write `smells.py`
  - [x] Function with too many parameters
  - [x] Deeply nested conditionals
  - [x] Dead store
  - [x] Class with excessive number of methods
- [x] Write `duplication.py` with two near-identical validation functions
- [x] Verify the app runs locally with `python main.py` and all endpoints respond

## Phase 2: Self-hosted analysis stack
- [x] Write `docker-compose.yml` with SonarQube Community Edition and Postgres 15 (validated with `docker compose config`)
- [ ] Run `docker compose up -d` and confirm the server becomes reachable at `localhost:9000`
- [ ] Log in, reset the default admin password
- [ ] Create a project in the SonarQube UI
- [ ] Generate a project analysis token

## Phase 3: Scan and verify
- [x] Write `sonar-project.properties` for the Python source
- [ ] Write and test the `docker run` command against `sonarsource/sonar-scanner-cli` (written as `run-scan.sh`; test after the server is up)
  - [ ] Confirm it reads `sonar-project.properties`
  - [ ] Confirm it authenticates using the generated token
- [ ] Run the first scan
- [ ] Verify Bugs findings appear on the dashboard
- [ ] Verify Vulnerabilities findings appear on the dashboard
- [ ] Verify Security Hotspots appear on the dashboard
- [ ] Verify Code Smells findings appear on the dashboard
- [ ] Verify Duplications percentage and block appear on the dashboard

## Phase 4: Documentation and walkthrough
- [x] Write README covering setup, running the app, running the scan, and viewing results
- [x] Add a mapping table: seed file to SonarQube category to what it demonstrates
- [x] Add mermaid diagrams to the README: architecture, scan flow, per-category issue maps, end-to-end demo flow
- [x] Review every file (code comments and documentation) to confirm no emojis appear anywhere (new project files verified clean)
- [ ] Do a full dry run as a new reader: clone to dashboard, using only the README

## Backlog / Unscheduled
- [ ] Wire SonarLens into a GitHub Actions workflow for scanning on push
- [ ] Add a remediated ("clean") counterpart to each seed file for a before/after comparison
- [ ] Consider extending the demo to a second language for cross-language coverage
