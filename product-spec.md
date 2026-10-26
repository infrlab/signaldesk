# Product specification — SignalDesk v1.0

**Problem:** Independent musicians and creative teams track press pitches in fragmented notes and email threads, making it easy to miss follow-ups and lose the overall picture.

**User:** One independent musician or team member managing a small release campaign.

**Goal:** Keep a structured synthetic/demo outreach pipeline; make it easy to see pitch progress and edit follow-ups in a local trusted environment.

## Functional acceptance criteria

1. Show summary cards (all, sent, replied, confirmed).
2. List every record's outlet, channel, status, follow-up date and note.
3. Search by outlet name with literal special-character handling.
4. Filter by status.
5. Add a new outlet and persist in SQLite.
6. Edit outlet metadata and status; allow clearing follow-up date.
7. Confirm before deletion; deleted rows do not reappear after refresh.
8. Validate required fields and reject invalid enum values and extra fields.
9. Provide OpenAPI documentation and operational health/aggregate metrics.
10. Public demonstration defaults to synthetic records, read-only endpoints, no login or private data.

**Non-goals:** Bulk emails, email harvesting, scraping, automatic pitches, real contacts, paid subscriptions, login, team collaboration, AI generated writing, file uploads.

**User stories:**
- As an artist, I want to see all outreach stages so I know what needs attention.
- As a manager, I want to add and update a prospect without editing a spreadsheet.
- As a reviewer, I want a safe public demonstration without exposing private artist information.

**Constraints:** Python 3.12, FastAPI, SQLite, vanilla frontend, Docker, CI. Local mode writable; public demo mode read-only. No external API keys.
