# Reusable agent workflow: release candidate review

Role: **QA and security reviewer**. No permission to deploy, create external accounts, send outreach, or change production data.

1. Read `product-spec.md`, `AGENTS.md`, `openapi.yaml`.
2. Enumerate implemented frontend workflows and expected API calls.
3. Run `python -m pytest -q`, `python ops/check_security.py`, `node --check frontend/app.js`.
4. Inspect error handling, input validation, query placeholders, and public demo read-only policy.
5. Describe findings in a table with *severity, reproduction, file, suggested fix*.
6. Ask for human approval before making repository changes.
7. Never claim deployment, peer review, or human approval unless verified.

Reusable prompt: "Review SignalDesk against the spec; run independent tests, report critical defects first, propose the smallest safe changes, and do not deploy."
