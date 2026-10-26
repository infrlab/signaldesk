# Deployment and course submission

## 1. Run locally with Docker

```bash
docker compose up --build -d
curl http://localhost:8000/health
```

Open `http://localhost:8000`. Records are writable and persisted in a named Docker volume (`signaldesk_data`). If you do not have Docker, install `requirements-dev.txt`, then `python -m uvicorn backend.app:app --reload`.

## 2. Make a new, public GitHub repository

Do **not** expose an existing private work repository. Create a **new public repository** named `signaldesk-zoomcamp-2026`. Upload this project's files, including dotfiles (GitHub Actions). Use Git CLI:

```bash
git init
git add .
git commit -m "Build SignalDesk full-stack portfolio project"
git branch -M main
git remote add origin https://github.com/USERNAME/signaldesk-zoomcamp-2026.git
git push -u origin main
git rev-parse HEAD
```

Replace USERNAME with the owner of the new repository. Do not invent a SHA; copy the exact 40-character output from `git rev-parse HEAD` after pushing. Verify public browsing while logged out.

## 3. Public demo hosting

`render.yaml` defines a container-based Render web service with synthetic demo seed. In Render, create a Blueprint from the public GitHub repo (review plan pricing before confirming). Set `READ_ONLY=true` and verify `GET /api/config` returns `read_only=true` after it is live. The sample is intentionally read-only because it has no user authentication. `DATABASE_PATH=/tmp/signaldesk.db` is ephemeral: persistence in the **local** Docker environment is durable, public demo re-seeds on restart.

Alternative hosts that run `docker build` or `uvicorn` also work; provide a writable persistent volume only behind proper auth. Set a health check on `/health`.

For **tests-gated deployment**, disable Render automatic deploys and add its deploy-hook URL as `RENDER_DEPLOY_HOOK_URL` under GitHub repository Settings → Secrets and variables → Actions. The GitHub Actions `deploy` job triggers the hook on successful main-branch CI. Without the secret, deploy does not run; this is intentional. Never paste hook URLs into code or commit history.

## 4. Validate online before submission

- Public URL opens without login and shows four **synthetic** records.
- `PUBLIC_URL/health` returns `{"status":"ok", "service":"signaldesk"}`.
- `PUBLIC_URL/api/config` reports read-only mode.
- GitHub Actions `Test and Audit` job is green.
- README includes your verified **public** URL and any screenshots you created. Do not make up a link.

## 5. Course submission

Open https://courses.datatalks.club/ai-dev-tools-2026/project/project1 and log in. Provide public GitHub URL, exact commit SHA, actual time spent, optional learning-in-public URL(s), and chosen certificate name. Review course rubric and complete required peer reviews by the cohort's dates.

**Submission is not automatic**. The app bundle and tests alone are not proof of a public repository, deployment, or course submission.
