# Intentionally Vulnerable Demo Application — Do Not Use in Production

## Overview
This repository contains a deliberately insecure Flask project named **Internal Employee Directory & Access Service**.

This repo is intended for **Checkmarx Developer Assist + Safe Refactor** demos, including dependency upgrades and consistent Flask import/usage updates across multiple files.

## Intended Vulnerabilities
- SQL injection in `/users` and `/login`
- Hard-coded secrets in `lab_app/config.py`
- Command injection in `/admin/ping`
- Debug mode enabled in `run.py`
- Pinned outdated dependencies for upgrade demonstrations

## Project Structure
```text
run.py
lab_app/
  __init__.py
  config.py
  db.py
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
### 1) Create a virtual environment
```bash
python -m venv .venv
```

### 2) Activate the virtual environment
macOS/Linux:
```bash
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

Windows (cmd.exe):
```cmd
.venv\Scripts\activate.bat
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Run the application
```bash
python run.py
```

The service listens on `http://127.0.0.1:5000` by default.

## Example curl commands
### Home
```bash
curl -s http://127.0.0.1:5000/
```

### Health
```bash
curl -s http://127.0.0.1:5000/health
```

### Query users
```bash
curl -s "http://127.0.0.1:5000/users?name=ad"
```

### Create user
```bash
curl -s -X POST http://127.0.0.1:5000/create-user \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"alicepass","role":"user"}'
```

### Login
```bash
curl -s -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"adminpass"}'
```

### Admin ping
```bash
curl -s "http://127.0.0.1:5000/admin/ping?host=127.0.0.1"
```

## Notes
- SQLite database file (`app.db`) is created automatically on first run.
- On first startup, two users are seeded:
  - `admin / adminpass / admin`
  - `user / userpass / user`
- Passwords are stored in plaintext intentionally for demonstration purposes.
