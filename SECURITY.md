# SECURITY — Threat Model & Controls (v4.3)

**Owner:** Jesse J. Lamont • **Org:** Lamont Labs • **Date:** 2025-10-05  
**Trademark:** MemoryCloud™ is a trademark of Jesse J. Lamont (not registered)

---

## Threat Model (Demo Scope)
| Threat | Vector | Control |
|---|---|---|
| Silent capture without consent | Background capture | **Fail-closed indicator gate** rejects when `indicator=false` |
| Tampering with stored events | Local file/db edits | **SHA-256 hash chain** + deterministic verifier |
| Data exfiltration | Network sync | **Offline-first**, no external services |
| Key leakage | Accidental commit | `.keys/` in `.gitignore`; generated locally |
| Replay / reorder | Appending old entries | Chain includes `prev_hash`; verifier detects inconsistency |

## Cryptography
- **Sealed-box** via PyNaCl (X25519/Curve25519) for encrypting payloads.
- **Ed25519** signatures for provenance (software-backed in demo).
- Hashing: **SHA-256** for chain continuity and checksums.

## Operational Controls
- No secrets committed to the repo.
- `verify.sh` validates chain integrity and checksums.
- Size limits and HTTP rejections for malformed payloads.

## Known Gaps (Demo)
- No hardware-backed keys (TEE/HSM).
- No auth/session management (single-user demo).
- No network ACLs (local host only).

## Next Steps
- Add key wrapping & rotation policy.
- Encrypted SQLite with per-record nonce & AEAD tags.
- Optional multi-tenant auth for pilot builds.

---
