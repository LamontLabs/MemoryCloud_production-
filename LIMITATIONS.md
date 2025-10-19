# MemoryCloud™ Limitations and Scope Notes
Owner: Jesse J. Lamont • Org: Lamont Labs • Version v4.3 • Date 2025-10-05  

---

## 1  Overview
This document defines the *known limitations, constraints, and exclusions*  
for the MemoryCloud™ demo build (v4.3).  
It is intended for investors, reviewers, and acquirers to understand what is deliberately out of scope.

---

## 2  Current Scope (Demo Build)
✅  Functional:
- Local capture (text / image / audio metadata stub)  
- Deterministic recall by semantic + timestamp ranking  
- Cryptographically signed audit log (append-only)  
- CLI HUD indicator system (✔ signed / ! fallback / ✖ invalid)  
- Full offline execution, no API dependencies

❌  Not Implemented:
- Cloud synchronization  
- Multi-device sync or streaming recall  
- Cross-user collaboration or shared vaults  
- AR or VisionOS HUD integration  
- Real-time transcription (stubbed only)  
- External identity or OAuth

---

## 3  Non-Compliance Statements
This project is **not** certified for any regulatory use (HIPAA, FERPA, GDPR).  
Compliance readiness is included in the roadmap, but no legal certification has occurred.  
Data is encrypted locally only; export controls are user-managed.

---

## 4  Performance
- Benchmark coverage: limited to ≤10K memory entries  
- Expected recall latency: ≤300 ms for top-5 results  
- Heavy-load and concurrency testing deferred until post-demo phase.  

---

## 5  Reliability
- Audit chain uses local file appends only (no distributed validation)  
- A power loss during append may require manual verification via `verify.sh`.  
- Key rotation and backup are manual operations in the current build.

---

## 6  Privacy Caveats
- All capture data remains local, but user must ensure device-level encryption.  
- Facial/voice redaction is not included.  
- GPS anchors (if enabled) are quantized to ~1 km precision, but may still expose coarse location if shared.

---

## 7  Security Gaps (Acknowledged)
- No HSM / TEE binding (software Ed25519 only)  
- No intrusion detection or telemetry  
- No integrity attestation beyond audit hash chain  
- Keys are not password-protected by default (intentionally simplified for demo)  

---

## 8  Known Edge Cases
| Case | Behavior | Resolution |
| :--- | :--- | :--- |
| Capture indicator off | Request rejected (HTTP 403) | Turn indicator ON |
| Upload > 10 MB | HTTP 413 | Compress or trim |
| Invalid signature | HUD shows ✖ | Re-generate keypair |
| Missing `.env` | Defaults used | Create `.env` from example |

---

## 9  Deferred Deliverables
These items are scheduled for the next milestone:
- Automated SBOM validation via CI  
- Public API docs with OpenAPI schema  
- Key rotation GUI  
- iOS/Android HUD prototype  
- Enterprise retention and DLP policies  

---

## 10  Disclaimer
This repository is a **demo and handoff-ready** artifact —  
not a production service.  
All assumptions and exclusions above are documented for audit transparency.

---

*Document frozen for v4.3 release — any production derivative must update this file.*
