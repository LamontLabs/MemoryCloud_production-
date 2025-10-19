# MemoryCloud™ Configuration Reference
Owner: Jesse J. Lamont • Org: Lamont Labs • Version v4.3 • Date 2025-10-05  

---

## 1  Overview
All configuration values are read from environment variables (via `python-dotenv`)  
and can be overridden at runtime through CLI flags or a `.env` file.  
This ensures deterministic behavior and safe reproducibility across systems.

---

## 2  Environment Variables
| Variable | Default | Description |
| :--- | :--- | :--- |
| `MC_ENV` | `dev` | Environment mode (`dev` / `demo` / `prod`) |
| `MC_DB` | `data/memorycloud.db` | SQLite database path |
| `MC_DATA_DIR` | `data/` | Directory for captured entries |
| `MC_KEY_PATH` | `.keys/memorycloud.key` | Private key for sealed-box crypto |
| `MC_PUB_PATH` | `.keys/memorycloud.pub` | Public key used for verification |
| `MC_AUDIT_LOG` | `provenance/audit.jsonl` | Append-only audit chain |
| `MC_HASH_ALGO` | `sha256` | Hash algorithm for provenance |
| `MC_MAX_FILE_MB` | `10` | Max upload size (MB) |
| `MC_RECALL_LIMIT` | `50` | Maximum records returned per recall query |
| `MC_RETENTION_DAYS` | `7` | Retention window before auto-deletion |
| `MC_LOG_LEVEL` | `INFO` | Log verbosity (`DEBUG` / `INFO` / `WARNING`) |
| `MC_PORT` | `8000` | API port binding |
| `MC_HOST` | `127.0.0.1` | Interface to bind |
| `MC_SBOM_PATH` | `SBOM/sbom.cdx.json` | CycloneDX output file |
| `MC_PROVENANCE_PATH` | `SBOM/provenance.json` | Provenance manifest |
| `MC_CHECKSUMS_PATH` | `SBOM/checksums.csv` | Checksum export |
| `MC_VERIFY_CMD` | `bash verify.sh` | Verification entrypoint |
| `MC_HUD_MODE` | `cli` | HUD type (`cli` / `api`) |
| `MC_HUD_INDICATOR` | `true` | Require capture indicator to be ON |
| `MC_OFFLINE_MODE` | `true` | Operate fully offline (no external calls) |
| `MC_SIGNING` | `ed25519` | Key algorithm for signatures |
| `MC_RELEASE_DIR` | `dist/` | Output directory for demo bundles |

---

## 3  Configuration Hierarchy
1. Environment variable  
2. `.env` file (loaded by `python-dotenv`)  
3. Runtime CLI argument (overrides previous values)  

Example:
```bash
MC_DB=/tmp/demo.db MC_LOG_LEVEL=DEBUG python src/memorycloud/main.py
```

---

## 4  Secrets and Keys
No secrets are committed to the repo.  
`.env.example` contains safe placeholders only.  
Real keys are auto-generated on first run and stored under `.keys/`.  

---

## 5  Deterministic Defaults
All defaults are explicit so that two clean runs produce identical config state.  
When `make verify` is executed, the system recomputes hashes of this file to confirm that no drift occurred.  

---

*Config revision verified and frozen for demo release 2025-10-05.*
