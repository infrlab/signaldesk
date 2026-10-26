# Security review — baseline findings, 2026-10-26

| Area | Finding | Mitigation / status |
|---|---|---|
| SQL injection | Parameterized values, fixed schema-derived update columns | Automated test includes hostile text and verifies table remains intact |
| XSS | Browser uses `textContent` for all user-controlled strings; no innerHTML | Manual code review, not a browser penetration test |
| Public mutation | No auth in current project | `READ_ONLY=true` in public blueprint; POST/PATCH/DELETE return 403; tested |
| Input bounds | Status/channel enum, outlet max 120, notes max 1000, q max 120, limit 1-100 | Pydantic validation; tested |
| Secret exposure | No API tokens, creds, or `.env` in repository | `.gitignore`, `ops/check_security.py` checks, manual review |
| Data persistence | SQLite durable in Docker volume, but Render's free /tmp is ephemeral | Not suitable for real production; preserve notes in architecture |
| Authentication / privacy | Not implemented | **Open requirement before any real-world deployment with personal data** |
| Dependency scanning | Deterministic source check only | Add Dependabot, pip-audit or other dependency checks in maintained deployment |

Run `python ops/check_security.py`. The output confirms only a limited deterministic source check, not a security certification.
