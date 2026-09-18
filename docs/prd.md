# SonarLens — Product Requirements Document

> Status: Draft | Last updated: 2026-09-18 | Owner: Siddhant Shukla

## 1. Overview
SonarLens is a small, deliberately messy demo application built to showcase every major issue category that SonarQube can detect: Bugs, Vulnerabilities, Security Hotspots, Code Smells, and Duplications. It runs entirely through Docker, using a self-hosted SonarQube Community Edition instance rather than SonarCloud, so the whole demo works offline with no external service dependency.

## 2. Problem Statement
Most SonarQube demos either use a real production codebase, where issues are scattered and hard to point to, or they only demonstrate one or two rule categories. There is no small, self-contained reference app where each SonarQube category has its own clearly labeled example, runnable end to end with nothing but Docker.

## 3. Goals
- Demonstrate all five SonarQube issue categories in one small, understandable codebase.
- Run the entire pipeline (analysis server, scanner, demo app) using only Docker, with no SonarCloud account or external network dependency.
- Make it easy to walk someone through the SonarQube dashboard and point at a real finding for each category.
- Keep the demo app itself simple enough that the seeded issues are the main point of interest, not the app's functionality.

## 4. Non-Goals
- This is not a production-grade task manager. Its features are intentionally minimal.
- This does not cover every possible SonarQube rule, only a representative example from each category.
- This does not include CI/CD automation in the first version; that is deferred (see Phases).
- This is not aimed at Enterprise Edition or SonarCloud-only rules (for example, some cross-file taint analysis in paid tiers).

## 5. Target Users / Personas
| Persona | Description | Primary need |
|---|---|---|
| Demo presenter | Siddhant, showing SonarQube capability to peers, a class, or a portfolio audience | A small, reliable app where every issue category is visibly represented |
| Workshop attendee | Someone learning what SonarQube actually flags and why | Clear, minimal, well-commented examples per category |

## 6. User Stories
- As a demo presenter, I want a single app where I can point to one file per issue category, so that I can explain each category without hunting through a large codebase.
- As a demo presenter, I want the entire analysis pipeline running in Docker, so that I do not depend on SonarCloud or any account outside my machine.
- As a workshop attendee, I want each seeded issue clearly commented in the source, so that I understand why SonarQube is flagging it.

## 7. Requirements

### 7.1 Functional Requirements
1. The system must provide a small Flask-based task manager application (add task, list tasks, get task by index, health check).
2. The system must include at least one deliberately seeded issue for each of the five SonarQube categories: Bugs, Vulnerabilities, Security Hotspots, Code Smells, Duplications.
3. The system must run a self-hosted SonarQube Community Edition server via Docker Compose, backed by a Postgres container.
4. The system must run static analysis using the official `sonarsource/sonar-scanner-cli` Docker image, pointed at the local SonarQube server.
5. The system must produce a dashboard in the local SonarQube UI (`http://localhost:9000`) showing findings in all five categories after a scan.
6. The system must document, per seeded issue, which category it belongs to and why SonarQube flags it.

### 7.2 Non-Functional Requirements
- The entire pipeline must run without any external SaaS dependency (no SonarCloud, no cloud database).
- Setup should require no more than: `docker compose up -d` for the server, and one `docker run` command for the scan.
- The demo app's own code should stay small enough to review in a single sitting (roughly 150 to 250 lines total across seed files).
- No emojis are to be used anywhere in the project's documentation or source comments.

## 8. Success Metrics
| Metric | Target | Timeframe |
|---|---|---|
| SonarQube categories represented on the dashboard | 5 out of 5 (Bugs, Vulnerabilities, Security Hotspots, Code Smells, Duplications) | After first scan |
| Manual setup steps required | 2 or fewer commands to go from clone to dashboard results | First run |
| External service dependencies | 0 | Ongoing |

## 9. Constraints & Assumptions
- Constraint: Must use self-hosted SonarQube Community Edition via Docker, not SonarCloud.
- Constraint: No emojis anywhere in documentation, code comments, or output.
- Assumption: Docker and Docker Compose are available on the demo machine.
- Assumption: Python 3.12 and Flask are an acceptable stack for the demo app (already familiar to the project owner).

## 10. Dependencies
- Docker Engine and Docker Compose.
- `sonarqube:community` Docker image.
- `postgres:15` Docker image (SonarQube's backing database).
- `sonarsource/sonar-scanner-cli` Docker image.

## 11. Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| SonarQube Community Edition does not cover every rule available in paid tiers, making the demo look incomplete | Medium | Low | Document clearly in the README which categories and languages are covered by Community Edition, and frame the demo around categories, not raw rule count |
| Seeded vulnerable code is mistaken for real production risk if the repo is reused elsewhere | Low | Medium | Clearly label every seed file as intentionally vulnerable/demo-only in both code comments and README |
| SonarQube container takes noticeably long to start on first boot, confusing first-time users | Medium | Low | Document the expected startup wait time in the README and provide a simple health-check step |

## 12. Open Questions
- [ ] Should a remediated ("clean") version of the app be included alongside the seeded version, to show a before/after scan comparison?
- [ ] Should this later be wired into a GitHub Actions workflow, or is it intended to stay a local-only demo?
