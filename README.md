# Intentionally Vulnerable Demo Application — Do Not Use in Production

## Overview
This repository contains a deliberately insecure Flask project named **Internal Employee Directory & Access Service**.

This repo is intended for **Checkmarx Developer Assist + Safe Refactor** demos, including dependency upgrades and repo-wide refactors around shared `urllib3` usage.

## Intended Vulnerabilities
- SQL injection in `/users` and `/login`
- Hard-coded secrets in `lab_app/config.py`
- Command injection in `/admin/ping`
- Debug mode enabled in `run.py`
- Pinned outdated dependencies for upgrade demonstrations

## Safe Refactor Demo Note
The app includes service modules that perform outbound HTTP operations. The pattern started as duplicated `urllib3` usage in multiple files, then is centralized via `lab_app/http_client.py` so Safe Refactor can demonstrate repo-wide updates from duplicated clients to a shared HTTP wrapper.

## Project Structure
```text
run.py
lab_app/
  __init__.py
  config.py
  db.py
  http_client.py
  services/
    __init__.py
    directory.py
    audit.py
    telemetry.py
  routes/
    __init__.py
    users.py
    auth.py
    admin.py
```

## API Endpoints
- `GET /` — home/health-style summary with endpoint list.
- `GET /health` — service status.
- `GET /users?name=<name>` — returns matching users (`id`, `username`, `role`).
- `POST /create-user` — JSON: `{ "username": "...", "password": "...", "role": "..." }`.
- `POST /login` — JSON: `{ "username": "...", "password": "..." }`.
- `GET /admin/ping?host=<host>` — executes ping and returns command output.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

The service listens on `http://127.0.0.1:5000` by default.

## Notes
- SQLite database file (`app.db`) is created automatically on first run.
- On first startup, two users are seeded:
  - `admin / adminpass / admin`
  - `user / userpass / user`
- Passwords are stored in plaintext intentionally for demonstration purposes.
