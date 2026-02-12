# Intentionally Vulnerable Demo Application — Do Not Use in Production

## Overview
This repository contains a deliberately insecure Flask project named **Internal Employee Directory & Access Service**.

This repo is intended for **demo and training use only** with **Checkmarx Developer Assist** and **Safe Refactor**.
It intentionally contains vulnerabilities and insecure coding patterns for scanner detection and remediation workflow demonstrations.
It must **not** be deployed to any real environment and must **not** be used with real data.

## What this app does
The API provides a small local employee directory and access service backed by SQLite:

- `GET /users?name=<name>` — list matching users.
- `POST /create-user` — create a user.
- `POST /login` — validate username/password.
- `GET /admin/ping?host=<host>` — run a ping command.

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
python app.py
```

The service listens on `http://127.0.0.1:5000`.

## Example curl commands
### Health check
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
- Passwords are stored in plaintext in this demo by design.
