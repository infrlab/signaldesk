# Architecture

```text
User browser
  ├─ GET / and /assets/*  → single-origin frontend (HTML/CSS/vanilla JS)
  └─ /api/*               → FastAPI (Pydantic input validation)
                                └─ database module → SQLite persisted at DATABASE_PATH
Operations: /health, /ops/metrics → health check and aggregate diagnostic counters
Delivery: Dockerfile → Docker Compose (local durable volume), GitHub Actions (CI), Render Blueprint (public READ_ONLY demo)
```

The frontend centralizes HTTP requests in the `api` object in `frontend/app.js`, preventing scattered endpoint implementations. Backend handlers validate JSON with Pydantic before calling SQLite. All row filters and values use bound SQL parameters; column names in update statements originate only from the declared patch schema. SQLite writes use managed transactions. The server runs same-origin; no CORS configuration is required.

## Why this stack

- **FastAPI**: typed request models; interactive docs at `/docs` and generated OpenAPI.
- **SQLite**: portable durable local storage without requiring paid cloud infrastructure.
- **Vanilla JS**: simple, accessible, mobile-friendly frontend with no build step.
- **Docker Compose**: one-command reproducible local system and persisted named volume.
- **GitHub Actions**: regression tests and deterministic audit on every push/PR.

## Constraints

No authentication or access controls are implemented for writable mode. **Do not expose writable mode publicly.** Production should introduce authentication, authorization, CSRF protections if cookie auth, backups and encrypted managed persistence before handling actual people or private media lists. The provided Render example is public and read-only, with synthetic seed data. Its `/tmp` database is ephemeral and not production persistence.
