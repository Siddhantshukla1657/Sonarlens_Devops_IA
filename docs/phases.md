# SonarLens — Phases

> Status: Draft | Last updated: 2026-09-18

## Roadmap Summary
| Phase | Name | Goal | Target duration |
|---|---|---|---|
| Phase 1 | Seeded demo application | A small runnable Flask app exists with one clearly labeled issue per SonarQube category | 1 to 2 days |
| Phase 2 | Self-hosted analysis stack | SonarQube Community Edition and Postgres run via Docker Compose, fully offline | 1 day |
| Phase 3 | Scan and verify | A scanner container successfully analyzes the app and the dashboard shows all five categories | 1 day |
| Phase 4 | Documentation and walkthrough | README and in-code comments make every seeded issue self-explanatory for a live demo | 1 day |

---

## Phase 1: Seeded demo application
**Goal:** Build the small Flask task manager with one seed file per SonarQube category.

**Scope:**
- `main.py` wiring together a minimal task manager (`/health`, `/tasks`, `/tasks/<idx>`).
- `bugs.py` with at least one real logic defect (for example, an off-by-one and a possible null dereference).
- `vulnerabilities.py` with at least one exploitable flaw (for example, command injection, weak hashing, SQL string concatenation).
- `hotspots.py` with code that requires manual security review (for example, disabled certificate verification, a hardcoded secret).
- `smells.py` with maintainability issues (for example, too many parameters, deep nesting, a class with too many responsibilities).
- `duplication.py` with two near-identical functions.

**Out of scope for this phase:**
- Any Docker or SonarQube setup.
- Fixing or remediating any of the seeded issues.

**Deliverables:**
- A runnable Flask app with all five seed files wired in.

**Dependencies:** None; this phase only needs Python and Flask locally.

**Exit criteria:** The app runs locally with `python main.py` and all endpoints respond as expected, including the seeded bug behavior.

---

## Phase 2: Self-hosted analysis stack
**Goal:** Stand up SonarQube Community Edition and its database entirely through Docker, with no external service dependency.

**Scope:**
- `docker-compose.yml` defining the SonarQube server and a Postgres 15 database.
- Initial manual setup steps documented: first login, password reset, project creation, token generation.

**Out of scope for this phase:**
- Running the actual scan (covered in Phase 3).
- Any CI/CD automation.

**Deliverables:**
- A working `docker compose up -d` that brings up a reachable SonarQube instance at `localhost:9000`.

**Dependencies:** Docker and Docker Compose installed locally.

**Exit criteria:** The SonarQube web UI is reachable at `localhost:9000` and a project token has been generated.

---

## Phase 3: Scan and verify
**Goal:** Run static analysis against the seeded app and confirm all five categories appear on the dashboard.

**Scope:**
- `sonar-project.properties` configured for the Python source.
- A documented `docker run` command (or a wrapping `run-scan.sh` script) using `sonarsource/sonar-scanner-cli`.
- Manual verification that Bugs, Vulnerabilities, Security Hotspots, Code Smells, and Duplications each show at least one finding.

**Out of scope for this phase:**
- Remediating any findings.

**Deliverables:**
- A successful scan whose dashboard shows findings in all five categories.

**Dependencies:** Phase 1 (seeded app) and Phase 2 (running SonarQube server) must both be complete.

**Exit criteria:** All five categories are visibly populated on the project dashboard after a single scan run.

---

## Phase 4: Documentation and walkthrough
**Goal:** Make the project self-explanatory for a live demo or portfolio review, with no emojis anywhere.

**Scope:**
- README covering setup, running the app, running the scan, and viewing results.
- A short mapping table in the README: seed file to SonarQube category to what it demonstrates.
- Final pass to confirm no emojis appear anywhere in documentation or code comments.

**Out of scope for this phase:**
- Any new code changes beyond documentation and comments.

**Deliverables:**
- A complete, plain-text README suitable for presenting the project.

**Dependencies:** Phases 1 through 3 complete.

**Exit criteria:** A new reader can go from cloning the repository to viewing all five categories on the dashboard using only the README.

---

## Future / Not Yet Scheduled
- Wiring SonarLens into a GitHub Actions workflow for automated scanning on push.
- Adding a remediated ("clean") version of each seed file to demonstrate a before/after comparison.
- Extending the demo to a second language to show cross-language coverage.
