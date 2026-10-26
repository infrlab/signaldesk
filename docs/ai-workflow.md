# AI-assisted development workflow — verifiable record

## Context and decomposition

The current AI Dev Tools Zoomcamp project requirements informed the scope. The project demonstrates an independent music outreach workflow using only synthetic records; it does not depend on production artist data. Development was organized into specification, API/backend, storage, frontend, tests, CI, packaging, security, operations and deployment documentation.

## Tool roles

- **Specification/PM (AI)**: interpreted the rubric; selected minimum scope; described the independent music outreach problem and privacy constraints.
- **Implementation (AI)**: authored FastAPI, SQLite, HTML/CSS/JavaScript, and packaging files.
- **Verification (AI + deterministic tools)**: ran Python compilation, API integration tests, data persistence tests, and security checks. Only actual passing results are recorded in `docs/qa-report.md`.
- **Independent review / publication**: public repository, deployment, course submission and peer reviews remain unverified until the corresponding systems confirm them.

## Representative prompts

- "Build a testable full-stack independent music outreach dashboard using a documented API and SQLite. Use synthetic data; no secrets or personal contact lists."
- "Check API create/list/update/delete, validation, filtering, persistence and read-only cloud safeguards using deterministic integration tests."
- "Compare the checked-in OpenAPI spec and the FastAPI-generated schema; do not claim public deployment if none is verified."

## Independent review protocol

1. Review `AGENTS.md` and `product-spec.md` before code changes.
2. Run `python -m pytest -q` and compare behavior with contract.
3. Run `python ops/check_security.py`; review manual findings.
4. Re-run checks after fixes, commit only after reproducible pass.
5. Verify deployment via live `/health`, `/api/summary`, and browser.

Generated and assisted code requires independent verification before deployment. Passing automated checks do not imply that a human review or public release has occurred.
