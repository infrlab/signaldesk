# Operations runbook

## Health check

`GET /health` responds `{status: 'ok', service: 'signaldesk'}` if the app is running. This does not guarantee database reachability. For DB health check, `GET /ops/metrics` returns aggregate record counters and uptime.

## When UI data disappears

1. Confirm `/health` and `/ops/metrics` independently.
2. Check backend logs from `docker compose logs signaldesk --tail=200`.
3. Check `DATABASE_PATH`, Docker named volume, read-only flag and environment change.
4. In a public Render demo `/tmp` is ephemeral by design. Re-seeding fake data is expected after restarts, **not a real-data persistence guarantee**.
5. If necessary, stop the system, back up the SQLite DB volume securely and re-run tests before modifying records.

## Incident boundaries

Do not auto-delete data, send notifications, change credentials, or give coding agents production write access. Limit incident response to observation and a human-approved change plan. No true monitoring/alerting service has been configured.
