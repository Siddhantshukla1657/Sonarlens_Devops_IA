# SonarLens — Feature List

> Status: Draft | Last updated: 2026-09-18

## Feature Summary
| # | Feature | Category | Phase | Priority | Status |
|---|---|---|---|---|---|
| 1 | Task manager core (add, list, get) | Application | Phase 1 | Must-have | Planned |
| 2 | Seeded Bugs example | Demo seed | Phase 1 | Must-have | Planned |
| 3 | Seeded Vulnerabilities example | Demo seed | Phase 1 | Must-have | Planned |
| 4 | Seeded Security Hotspots example | Demo seed | Phase 1 | Must-have | Planned |
| 5 | Seeded Code Smells example | Demo seed | Phase 1 | Must-have | Planned |
| 6 | Seeded Duplications example | Demo seed | Phase 1 | Must-have | Planned |
| 7 | Self-hosted SonarQube stack | Infrastructure | Phase 2 | Must-have | Planned |
| 8 | Dockerized scanner run | Infrastructure | Phase 3 | Must-have | Planned |
| 9 | README walkthrough and category mapping | Documentation | Phase 4 | Must-have | Planned |

*Priority: Must-have / Should-have / Nice-to-have. Status: Planned / In progress / Done.*

---

## 1. Task manager core
**Category:** Application
**Phase:** Phase 1
**Priority:** Must-have

**What it does:**
Provides a minimal in-memory task manager (add a task, list tasks, fetch a task by index, health check) so the seeded issues live inside a real, runnable application rather than disconnected scripts.

**User story:**
As a demo presenter, I want a small working application, so that the seeded issues appear inside real, running code rather than isolated snippets.

**How it works:**
1. Trigger: an HTTP request to one of the four endpoints.
2. Logic: `/tasks` (POST) appends a title to an in-memory list; `/tasks` (GET) returns the full list; `/tasks/<idx>` (GET) looks up a single task by index using the seeded `get_item` function; `/health` returns a status object that also exposes the current debug flag.
3. Result: the caller receives a JSON response reflecting the current in-memory task state.

**Inputs:** JSON body with a `title` field (for POST), an integer index (for GET by index).

**Outputs:** JSON responses; in-memory task list state.

**Edge cases & error handling:**
- Edge case: index equal to the list length → seeded off-by-one bug in `get_item` allows this through when it should not.
- Edge case: empty task list → `/tasks` returns an empty JSON array.

**Dependencies:** Flask.

---

## 2. Seeded Bugs example
**Category:** Demo seed
**Phase:** Phase 1
**Priority:** Must-have

**What it does:**
Contains real logic defects that SonarQube classifies as Bugs: a division with no zero-check, an off-by-one comparison in `get_item`, and a possible null dereference in a value-printing helper.

**User story:**
As a demo presenter, I want a file with genuine logic defects, so that I can show what SonarQube flags as a Bug versus a Code Smell.

**How it works:**
1. Trigger: static analysis scan reads `bugs.py`.
2. Logic: SonarQube's Python rule set detects the zero-division risk, the off-by-one boundary condition, and the potential attribute access on a `None` value.
3. Result: three or more findings appear under the Bugs category on the dashboard, each traceable to a specific line in `bugs.py`.

**Inputs:** None beyond the source file itself during a scan.

**Outputs:** Bug findings on the SonarQube dashboard.

**Edge cases & error handling:**
- Edge case: these are intentionally left unfixed, since demonstrating the bug is the feature's purpose.

**Dependencies:** SonarQube Python analyzer.

---

## 3. Seeded Vulnerabilities example
**Category:** Demo seed
**Phase:** Phase 1
**Priority:** Must-have

**What it does:**
Contains exploitable security flaws that SonarQube classifies as Vulnerabilities: shell command execution built from unsanitized input, an MD5-based password hash, and a SQL query built through string concatenation.

**User story:**
As a demo presenter, I want a file with real exploitable flaws, so that I can show the difference between a Vulnerability and a Security Hotspot.

**How it works:**
1. Trigger: static analysis scan reads `vulnerabilities.py`.
2. Logic: SonarQube detects the command injection pattern, the use of a weak hashing algorithm, and the string-concatenated SQL query.
3. Result: findings appear under the Vulnerabilities category, each with a severity rating and remediation guidance in the dashboard.

**Inputs:** None beyond the source file itself during a scan.

**Outputs:** Vulnerability findings on the SonarQube dashboard.

**Edge cases & error handling:**
- Edge case: this file must never be wired into any externally reachable endpoint, to avoid the demo becoming an actual exploitable service.

**Dependencies:** SonarQube Python analyzer.

---

## 4. Seeded Security Hotspots example
**Category:** Demo seed
**Phase:** Phase 1
**Priority:** Must-have

**What it does:**
Contains code that SonarQube flags for manual security review rather than an automatic failure: disabled TLS certificate verification, a debug flag left enabled, and a hardcoded secret key.

**User story:**
As a demo presenter, I want a file that triggers Security Hotspots specifically, so that I can explain how Hotspots differ from Vulnerabilities in requiring human judgment.

**How it works:**
1. Trigger: static analysis scan reads `hotspots.py`.
2. Logic: SonarQube flags the disabled certificate verification, the hardcoded secret, and the debug flag as items needing manual "Safe" or "Fix" review rather than treating them as confirmed defects.
3. Result: findings appear under the Security Hotspots tab, each requiring a reviewer decision in the dashboard.

**Inputs:** None beyond the source file itself during a scan.

**Outputs:** Security Hotspot entries on the SonarQube dashboard, pending review status.

**Edge cases & error handling:**
- Edge case: hotspots do not fail a quality gate by default the way Vulnerabilities can, which is itself a useful point to demonstrate.

**Dependencies:** SonarQube Python analyzer.

---

## 5. Seeded Code Smells example
**Category:** Demo seed
**Phase:** Phase 1
**Priority:** Must-have

**What it does:**
Contains maintainability issues that SonarQube classifies as Code Smells: a function with too many parameters, deeply nested conditionals, a dead store, and a class with an excessive number of methods.

**User story:**
As a demo presenter, I want a file focused purely on maintainability issues, so that I can distinguish Code Smells from Bugs and Vulnerabilities.

**How it works:**
1. Trigger: static analysis scan reads `smells.py`.
2. Logic: SonarQube's complexity and maintainability rules flag the parameter count, nesting depth, dead store, and the oversized class.
3. Result: findings appear under the Code Smells category, typically with a lower severity than Bugs or Vulnerabilities.

**Inputs:** None beyond the source file itself during a scan.

**Outputs:** Code Smell findings on the SonarQube dashboard.

**Edge cases & error handling:**
- Edge case: none of these issues affect runtime correctness, which is itself part of the point being demonstrated.

**Dependencies:** SonarQube Python analyzer.

---

## 6. Seeded Duplications example
**Category:** Demo seed
**Phase:** Phase 1
**Priority:** Must-have

**What it does:**
Contains two near-identical email validation functions so SonarQube's duplication detector has a clear, deliberate block of repeated logic to report.

**User story:**
As a demo presenter, I want a file with a clear duplicated block, so that I can show the duplication percentage metric on the dashboard.

**How it works:**
1. Trigger: static analysis scan reads `duplication.py`.
2. Logic: SonarQube's duplication engine compares token sequences across functions and detects the near-identical block shared between `validate_email_a` and `validate_email_b`.
3. Result: the file's duplication percentage rises, and the specific duplicated block is highlighted in the dashboard's duplications view.

**Inputs:** None beyond the source file itself during a scan.

**Outputs:** Duplication percentage and highlighted duplicated block on the SonarQube dashboard.

**Edge cases & error handling:**
- Edge case: duplication is measured at the token level, so even renamed variables inside an otherwise identical block will still be detected.

**Dependencies:** SonarQube Python analyzer.

---

## 7. Self-hosted SonarQube stack
**Category:** Infrastructure
**Phase:** Phase 2
**Priority:** Must-have

**What it does:**
Runs SonarQube Community Edition and its Postgres database entirely through Docker Compose, so the whole analysis server exists locally with no SonarCloud account or external network call.

**User story:**
As a demo presenter, I want the analysis server to run fully offline, so that the demo works without any external account or internet dependency.

**How it works:**
1. Trigger: running `docker compose up -d`.
2. Logic: Compose starts the Postgres container first, then the SonarQube server container, which connects to Postgres over the internal Docker network.
3. Result: the SonarQube web UI becomes reachable at `http://localhost:9000` after the server finishes initializing.

**Inputs:** None beyond the `docker-compose.yml` file itself.

**Outputs:** A running SonarQube server and database, reachable locally.

**Edge cases & error handling:**
- Edge case: first startup can take roughly a minute; documented in the README rather than treated as a failure.

**Dependencies:** Docker Engine and Docker Compose.

---

## 8. Dockerized scanner run
**Category:** Infrastructure
**Phase:** Phase 3
**Priority:** Must-have

**What it does:**
Runs the official `sonarsource/sonar-scanner-cli` Docker image against the mounted SonarLens source, pushing analysis results to the local SonarQube server.

**User story:**
As a demo presenter, I want to trigger a full scan with a single command, so that the demo stays fast and repeatable.

**How it works:**
1. Trigger: running the documented `docker run` command (or `run-scan.sh`).
2. Logic: the scanner container reads `sonar-project.properties`, analyzes the mounted source tree, and authenticates to the local server using a project token passed as an environment variable.
3. Result: the SonarQube dashboard updates with fresh findings across all five categories.

**Inputs:** `SONAR_HOST_URL`, `SONAR_TOKEN`, mounted source directory, `sonar-project.properties`.

**Outputs:** Updated analysis results on the SonarQube dashboard.

**Edge cases & error handling:**
- Edge case: an invalid or expired token causes the scan to fail with a clear authentication error in the console output.

**Dependencies:** A running SonarQube server (Feature 7) and a valid project token.

---

## 9. README walkthrough and category mapping
**Category:** Documentation
**Phase:** Phase 4
**Priority:** Must-have

**What it does:**
Documents setup, running the app, running the scan, and viewing results, including a table mapping each seed file to the SonarQube category it demonstrates.

**User story:**
As a workshop attendee, I want a clear written walkthrough, so that I can reproduce the demo and understand each finding without additional explanation.

**How it works:**
1. Trigger: a new reader opens the README.
2. Logic: the README walks through cloning the repository, starting the Docker stack, running the scanner, and opening the dashboard, with a table linking each seed file to its category and a one-line explanation of the flagged issue.
3. Result: a reader can go from a fresh clone to viewing all five categories on the dashboard without needing to ask follow-up questions.

**Inputs:** None; this is a documentation feature.

**Outputs:** A complete README file.

**Edge cases & error handling:**
- Edge case: none; this feature is purely documentation.

**Dependencies:** Features 1 through 8 must be complete and stable before the README is finalized.

---

## Deferred / Future Features
- GitHub Actions integration for automated scanning on push — deferred until the local-only demo is fully stable.
- A remediated ("clean") counterpart to each seed file for a before/after comparison — deferred as a possible Phase 5 addition.
