# Optional agent integration / MCP adapter

The application already provides a documented read-only API at `GET /api/summary` and `GET /api/contacts`.
An MCP tool `list_outreach_summary` can wrap `GET /api/summary`, exposing only aggregate demo status counts.

Proposed tool schema: `{}` (no arguments). Result: `{total: number, by_status: object, overdue: number}`.
An MCP adapter should run inside a controlled network context and allowlist the base URL.
Do not expose write APIs to a general-purpose agent. This is a **design sketch**, not a deployed MCP server; it receives no rubric credit for an implemented server.
