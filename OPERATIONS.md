# MemoryCloud™ Operations Manual
Owner: Jesse J. Lamont • Org: Lamont Labs • Version v4.3 • Date 2025-10-05

---

## 1  Overview
MemoryCloud™ runs entirely offline and stores encrypted “memory cards” (JSON blobs) in a local SQLite database.  
Each capture is cryptographically sealed, logged in a hash-chained audit file, and exposed through FastAPI endpoints.

This document describes how to operate the demo instance, rotate keys, and back up or restore data safely.

---

## 2  Run Modes
| Mode | Command | Purpose |
| :--- | :--- | :--- |
| Development | `uvicorn src.memorycloud.main:app --reload` | Hot-reload for local testing |
| Demo | `make run` | Run with deterministic seed data |
| Verify | `make verify` | Regenerate hashes + SBOM and confirm reproducibility |
| Release | `make release` | Bundle ZIP for investor/demo handoff |

---

## 3  Data Storage & Rotation
- Database: `data/memorycloud.db` (SQLite)  
- Audit Logs: `provenance/audit.jsonl`  
- Exports: `dist/audit_exports/*.jsonl`  

Rotation Policy (Recommended):  
```bash
# Daily rollover of audit logs and hash chain root
bash scripts/rotate_audit.sh
```
Keep at least 7 days of logs; older may be archived or encrypted off-device.

---

## 4  Key Management
- Primary keypair generated on first run → `.keys/memorycloud.key`  
- Public key included in every provenance entry  
- Rotation: `make rotate-keys` (regenerates pair and re-seals new records)  
Always back up `.keys/` securely before rotation.

---

## 5  Backups
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz data/ provenance/ .keys/
```
Restore by extracting and pointing `MC_DATA_DIR` in `.env` to the restored path.

---

## 6  Monitoring and Logs
- HTTP logs → `logs/access.log` (Uvicorn standard)  
- App events → `logs/app.log`  
- Hash failures or security flags → `logs/security.log`  

Use `tail -f logs/app.log` for real-time view.

---

## 7  Shutdown / Restart
Graceful shutdown (`Ctrl +C`) ensures the audit chain flushes and hash roots are sealed.  
After restart, verify integrity:
```bash
bash verify.sh
```
The script exits `0` if the chain is consistent.

---

## 8  Disaster Recovery
If the audit chain is corrupted:  
1. Stop the server.  
2. Inspect `provenance/audit.jsonl` for the last valid record.  
3. Run `python -m src.memorycloud.provenance --rebuild audit.jsonl`.  
4. Compare hash root to previous checkpoint.

---

## 9  Maintenance Schedule
| Task | Frequency | Owner |
| :--- | :--- | :--- |
| Verify audit chain | Daily | Ops Lead |
| Rotate keys | Monthly | Security |
| Backup DB + logs | Weekly | Ops |
| Run `make verify` | Before release | Maintainer |

---

**All operations must preserve determinism.**  
If outputs change unexpectedly, flag the build as non-deterministic and investigate.

---
