# Agent instructions — SignalDesk

You are maintaining a synthetic-data educational application, not a production CRM.

1. Read `product-spec.md`, `docs/architecture.md`, `docs/permissions.md` before changing code.
2. Preserve the `/api/contacts`, `/api/summary`, `/api/config`, `/health`, and `/ops/metrics` contracts; update `openapi.yaml` and tests on any route change.
3. No personal information, real artists' private contact lists, hidden credentials, cloud API keys, or email sending integrations.
4. Keep SQLite SQL parameters bound. No arbitrary SQL from browser input. Render dynamic text via `textContent`.
5. Public deployments MUST set `READ_ONLY=true` until proper auth has been independently reviewed.
6. Run `python -m pytest -q`, `python ops/check_security.py`, and `node --check frontend/app.js` after edits.
7. Use focused commits and record reproducible QA results. Do not claim public deployment or user submission unless verified.
8. Never autonomously send emails, publish personal materials, or change billing.
