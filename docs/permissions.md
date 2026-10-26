# Permission boundaries

- Browser: read aggregate demo counts and records; local-only create/modify/delete when `READ_ONLY=false`.
- Backend: SQLite operations, no outgoing emails, no third-party API credentials, no filesystem writes beyond SQLite.
- AI developer: may read code/spec, recommend tests, report vulnerabilities; requires human approval before writing to remote code, changing hosts, or sending messages.
- Optional future agent tool: read-only `GET /api/summary`; no permission to list private contact notes on a public agent.
- Public demo: read-only and synthetic only. No real outreach names, emails, addresses, keys, contracts or release plans.
