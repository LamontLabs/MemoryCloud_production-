# PRIVACY — Data Handling & Retention (v4.3)

**Owner:** Jesse J. Lamont • **Org:** Lamont Labs • **Date:** 2025-10-05  
**Trademark:** MemoryCloud™ is a trademark of Jesse J. Lamont (not registered)

---

## Principles
- **Local-first:** All data remains on device for the demo.
- **Minimal retention:** Defaults to 7 days (configurable via `MC_RETENTION_DAYS`).
- **User control:** Exports are local files; user decides what to share.
- **Transparency:** Audit chain records actions and provides verifiable integrity.

## Data Types
- **Memory content:** Text + optional metadata; encrypted at rest.
- **Provenance:** Timestamps, action, payload hash; no raw content.
- **Keys:** Local keypair stored under `.keys/`, excluded from repo.

## Retention & Deletion
- Automatic cleanup routine can purge records older than `MC_RETENTION_DAYS`.
- Manual purge via SQLite and audit-append for deletion events (logged).

## Export
- `GET /audit/export` returns JSONL for external verification.
- `src/memorycloud/export.py` provides JSON (and demo PDF) exports.

## What We Do NOT Do
- No cloud uploads.
- No third-party API sharing.
- No selling of data.

---
