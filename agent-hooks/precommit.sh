#!/usr/bin/env bash
set -euo pipefail
python -m compileall -q backend
python ops/check_security.py
python -m pytest -q
printf 'Agent safety/quality hook: OK\n'
