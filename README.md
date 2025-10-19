# path: README.md
# MemoryCloud™ — Privacy-First AI Memory Assistant
Owner: Jesse J. Lamont • Org: Lamont Labs • Version: v4.3 • Date: 2025-10-05  
Status: Demo-ready backend • Stack: Python 3.11 + FastAPI + SQLite + PyNaCl

---

### Purpose
MemoryCloud™ is a deterministic, privacy-first recall system.  
It captures text / audio / image metadata locally, encrypts each record, and stores
append-only provenance logs with SHA-256 chaining.

### Features
- 🔒 **Sealed-box encryption** (PyNaCl)
- 🧭 **Fail-closed indicator gating** (✔ = signed / ! = fallback / ✖ = rejected)
- 📜 **Provenance JSONL logs** with hash verification
- 🧠 **Deterministic recall API** (hybrid semantic + recency ranking)
- 🪶 **Lightweight SQLite store** for offline mode
- ⚙️ **Verify script** + **CycloneDX SBOM** for reproducibility

### Quick Start
```bash
git clone https://github.com/Lamont-Labs/memorycloud
cd memorycloud
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.memorycloud.main:app --reload
```
Then visit → [http://localhost:8000/docs](http://localhost:8000/docs)

### Demo Flow
1. `POST /capture` → Encrypt + store event  
2. `GET /recall` → Deterministic ranked recall  
3. `GET /audit/export` → Download hash-chained provenance log  
4. Run `bash verify.sh` → Validate deterministic outputs  

---

**Pointers**  
- Setup → [INSTALL.md](INSTALL.md)  
- Operations → [OPERATIONS.md](OPERATIONS.md)  
- Provenance → [PROVENANCE.md](PROVENANCE.md)  
- Security → [SECURITY.md](SECURITY.md)  
- Limitations → [LIMITATIONS.md](LIMITATIONS.md)  
- Contact → [CONTACT.md](CONTACT.md)

---

© 2025 Jesse J. Lamont.  
MemoryCloud™ is a trademark of Jesse J. Lamont (not registered).  
Licensed under MIT.
