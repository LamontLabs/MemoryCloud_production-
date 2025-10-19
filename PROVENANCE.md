# PROVENANCE — Determinism & Audit Verification (v4.3)

**Owner:** Jesse J. Lamont • **Org:** Lamont Labs • **Date:** 2025-10-05  
**Trademark:** MemoryCloud™ is a trademark of Jesse J. Lamont (not registered)

---

## What We Hash
- All tracked repository files (via `git ls-files` fallback to `find`), sorted deterministically.
- Outputs are written to `SBOM/checksums.csv` (format: `sha256,relative_path`).
- A root hash of the checksums CSV is written to `provenance/root_hash.txt`.

## Audit Chain Integrity
- Every capture appends a JSON record to `provenance/audit.jsonl` (or `dist/audit_exports/audit.jsonl`).
- Each record contains: `ts`, `action`, `payload_hash`, `prev_hash`, and `hash`.
- The `hash` is `SHA256(ts + action + payload_hash + prev_hash)`; the first record uses empty `prev_hash`.
- Chain validity is confirmed by `verify.sh` and `/audit/export`.

## How to Verify (Local)
```bash
bash verify.sh
# Outputs:
# - SBOM/checksums.csv
# - provenance/root_hash.txt
# - SBOM/provenance.json (manifest)
# - SBOM/sbom.cdx.json (CycloneDX SBOM)
