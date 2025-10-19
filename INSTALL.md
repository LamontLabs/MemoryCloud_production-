# MemoryCloud™ Installation Guide

Owner: Jesse J. Lamont • Org: Lamont Labs • Version v4.3 • Date 2025-10-05

---

## 1 — Requirements
- Python ≥ 3.11  
- SQLite 3.x  
- Git  
- bash / zsh / PowerShell  
- (optional) `make` for shortcuts  
- Internet access only for dependency install — runtime works fully offline.

---

## 2 — Setup (virtual environment)
```bash
git clone https://github.com/Lamont-Labs/memorycloud
cd memorycloud
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3 — Configuration
All environment variables are described in [CONFIG.md](CONFIG.md).  
A ready-made `.env.example` is provided — copy it and edit paths if desired:
```bash
cp .env.example .env
```

---

## 4 — Run Server
```bash
uvicorn src.memorycloud.main:app --reload
```
API Docs → [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 5 — Makefile Shortcuts
| Command | Description |
| :--- | :--- |
| `make setup` | Install and init SQLite DB |
| `make run` | Run FastAPI locally |
| `make verify` | Rebuild hashes + SBOM |
| `make test` | Run pytest |
| `make release` | Create ZIP demo bundle |

---

## 6 — First Demo
```bash
curl -X POST http://127.0.0.1:8000/capture -H "Content-Type: application/json" \
-d '{"text":"MemoryCloud demo entry","indicator":true}'
```
```bash
curl http://127.0.0.1:8000/recall
```

---

## 7 — Uninstall / Cleanup
```bash
deactivate
rm -rf .venv __pycache__ dist logs
```

---

*All steps tested 2025-10-05 on Ubuntu 22.04 and macOS 14.*
