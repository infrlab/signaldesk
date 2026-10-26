# SignalDesk

**A simple place to track music outreach, from the first pitch to the last follow-up.**

Independent releases often involve dozens of conversations with blogs, radio shows, playlist curators and venues. SignalDesk brings those conversations into one small dashboard so that it is easier to see what has been sent, what needs a reply and what comes next.

This is a working course project, **not** a production mailing list or a connected CRM. All example outlets and notes are fictional. No artist contacts, personal correspondence or private account data are included.

## What it does

- Shows the outreach pipeline at a glance, with counters for total, sent, replied and confirmed.
- Lets you add, edit and delete records in a local installation.
- Searches outlets and filters by status.
- Saves records in SQLite rather than browser memory.
- Serves a documented FastAPI backend and a responsive HTML/CSS/JavaScript frontend.
- Switches to **read-only mode** for public demos, because authentication has not been implemented.

## See it locally

You will need Docker and Docker Compose.

```sh
docker compose up --build
```

Visit **http://localhost:8000** to use the app and **http://localhost:8000/docs** to explore its API. The local Docker volume keeps records between restarts. The example records are fictional and can be edited locally.

Prefer to run Python directly?

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m uvicorn backend.app:app --reload
```

## Run the checks

```sh
python -m pytest -q
python ops/check_security.py
node --check frontend/app.js
```

The test suite covers core API operations, validation, search, persistence and read-only restrictions. See [the QA report](docs/qa-report.md) for executed checks and the limits of the review.

## Under the hood

| Part | Choice | Why |
| --- | --- | --- |
| Interface | HTML, CSS and JavaScript | Lightweight, straightforward to inspect |
| API | FastAPI + Pydantic | Clear routes, validation and generated API docs |
| Storage | SQLite | Simple durable data for a local prototype |
| Local runtime | Docker Compose | Reproducible setup and named data volume |
| CI | GitHub Actions | Run tests and source checks on changes |
| Demo deployment | Render blueprint | Optional public read-only preview |

The API supports contact listing, creation, updates and deletion, plus an outreach summary and health endpoints. The [OpenAPI contract](openapi.yaml) and [architecture notes](docs/architecture.md) document the interface and implementation choices.

## Current status and limitations

**Verified locally:** Python tests, JavaScript syntax checks and a limited source-security audit. The project is prepared for Docker-based deployment.

**Not yet verified:** live hosting, production monitoring, human accessibility testing or submission to the course. A hosted demo must set `READ_ONLY=true`. The current application has no authentication, so it must not hold real contact information on a public server.

Deployment steps are in [docs/deployment.md](docs/deployment.md). Operational notes and security boundaries live in [ops/runbook.md](ops/runbook.md) and [security/audit.md](security/audit.md).

## Coursework and development notes

Built as a portfolio exercise for the **DataTalks.Club AI Dev Tools Zoomcamp 2026**. The course requires evidence of an AI-assisted engineering workflow; that context, sample instructions and verification process are recorded in [docs/ai-workflow.md](docs/ai-workflow.md). These notes describe what was done rather than attributing unperformed review or deployment steps to anyone.

The repository also contains [project instructions](AGENTS.md), [agent-extension notes](docs/agent-extension-pack.md) and a [permissions policy](docs/permissions.md). Proposed integrations are described as proposals, not functioning services.

MIT licensed. See [LICENSE](LICENSE).
