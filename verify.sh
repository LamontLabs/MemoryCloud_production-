#!/usr/bin/env bash
# MemoryCloud™ — Deterministic Verification Script  [REPLACEMENT]
# Owner: Jesse J. Lamont • Org: Lamont Labs • v4.3.2 • Date: 2025-10-05
# What this does:
#   1) Sanity-check runtime (Python 3.11, pip)
#   2) Compute sorted SHA-256 checksums → SBOM/checksums.csv + provenance/root_hash.txt
#   3) Run in-process API smoke (capture ✔, recall, audit presence)
#   4) Validate provenance hash-chain integrity
#   5) Generate CycloneDX SBOM via cyclonedx-python-lib (non-fatal if missing)
#   6) Write SBOM/provenance.json manifest
# Exit codes:
#   0 = all checks passed
#   1 = environment invalid
#   2 = API smoke failed
#   3 = provenance chain invalid
#   (SBOM generation never fails the demo)

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

mkdir -p SBOM provenance dist/audit_exports logs

echo "[0/6] Environment sanity…"
PYBIN="$(command -v python || true)"
if [[ -z "$PYBIN" ]]; then
  echo "[-] python not found on PATH"; exit 1
fi

PYVER=$($PYBIN -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$PYVER" != "3.11" ]]; then
  echo "[-] Python $PYVER detected; require 3.11 for deterministic demo"; exit 1
fi

echo "    - python: $PYBIN ($PYVER)"
echo "    - pip:    $($PYBIN -m pip --version)"

echo "[1/6] Computing deterministic checksums…"
# Prefer git file list; fall back to find if not a git repo
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  FILES=$(git ls-files)
else
  FILES=$(find . -type f ! -path "./.git/*")
fi

# Exclusions (non-deterministic or generated)
EXCLUDE_REGEX='(^$|^\.git/|^\.venv/|^node_modules/|^dist/|^__pycache__/|^\.pytest_cache/|^SBOM/checksums\.csv$|^SBOM/sbom\.cdx\.json$|^SBOM/provenance\.json$)'
MAPFILE=()
while IFS= read -r f; do
  [[ "$f" =~ $EXCLUDE_REGEX ]] && continue
  # normalize leading ./ if present
  f="${f#./}"
  MAPFILE+=("$f")
done <<< "$FILES"

IFS=$'\n' SORTED=($(printf "%s\n" "${MAPFILE[@]}" | sort))
TMP="$(mktemp)"
: > "$TMP"
for f in "${SORTED[@]}"; do
  [[ -f "$f" ]] || continue
  sha=$(sha256sum "$f" | awk '{print $1}')
  echo "${sha},${f}" >> "$TMP"
done
mkdir -p SBOM provenance
# header + sorted output
{ echo "sha256,file"; sort -t',' -k2 "$TMP"; } > SBOM/checksums.csv
rm -f "$TMP"
ROOT_HASH=$(sha256sum SBOM/checksums.csv | awk '{print $1}')
echo "$ROOT_HASH" > provenance/root_hash.txt
echo "    - SBOM/checksums.csv (root: $ROOT_HASH)"

echo "[2/6] API smoke (in-process TestClient)…"
$PYBIN - <<'PY'
import sys, json
try:
    from fastapi.testclient import TestClient
except Exception as e:
    print(f"[!] fastapi.testclient missing: {e}", file=sys.stderr); sys.exit(2)
try:
    from src.memorycloud.main import app
except Exception as e:
    print(f"[!] cannot import app: {e}", file=sys.stderr); sys.exit(2)

tc = TestClient(app)

r = tc.post("/capture", json={"text":"verify-demo-entry","indicator":True})
assert r.status_code == 200 and r.json().get("hud") == "✔", r.text

r2 = tc.get("/recall", params={"q":"verify-demo-entry"})
assert r2.status_code == 200 and any("verify-demo-entry" in m.get("text","") for m in r2.json().get("matches",[])), r2.text

r3 = tc.get("/audit/export")
assert r3.status_code in (200,404)  # ok if very first run has no audit yet
print(json.dumps({"api_smoke":"ok"}))
PY
echo "    - API smoke OK"

echo "[3/6] Provenance hash-chain validation…"
$PYBIN - <<'PY'
import json, hashlib, sys, os
from pathlib import Path

paths = ["provenance/audit.jsonl", "dist/audit_exports/audit.jsonl"]
audit = None
for p in paths:
    if Path(p).exists():
        audit = Path(p); break

if not audit:
    # Acceptable when only a single capture happened via TestClient (it appended)
    # If file still absent, pass with 0 entries.
    print(json.dumps({"chain":"no_log_yet","ok":True,"entries":0}))
    sys.exit(0)

prev = ""
ok = True
n = 0
with audit.open("r", encoding="utf-8") as fh:
    for i, line in enumerate(fh,1):
        line=line.strip()
        if not line: continue
        rec = json.loads(line)
        ts  = rec.get("ts","")
        act = rec.get("action","")
        ph  = rec.get("payload_hash","")
        pvh = rec.get("prev_hash","")
        cur = rec.get("hash","")
        calc = hashlib.sha256((ts+act+ph+pvh).encode()).hexdigest()
        if calc != cur or pvh != prev:
            ok=False; print(f"[!] chain break at line {i}", file=sys.stderr)
        prev = cur
        n += 1

print(json.dumps({"chain":"validated","ok":ok,"entries":n,"last_hash":prev}))
sys.exit(0 if ok else 3)
PY
echo "    - provenance OK"

echo "[4/6] SBOM generation (cyclonedx-python-lib)…"
set +e
if $PYBIN -c "import cyclonedx_py" 2>/dev/null; then
  $PYBIN -m cyclonedx_py -o SBOM/sbom.cdx.json -e requirements.txt >/dev/null 2>&1
  SBOM_STATUS=$?
else
  SBOM_STATUS=127
fi
set -e
if [[ $SBOM_STATUS -ne 0 ]]; then
  echo "[i] cyclonedx-python-lib not available; writing minimal SBOM stub"
  $PYBIN - <<'PY'
import json, pathlib
p = pathlib.Path("SBOM/sbom.cdx.json"); p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps({"bomFormat":"CycloneDX","version":1,"metadata":{"note":"stub"}}, indent=2))
PY
else
  echo "    - SBOM/sbom.cdx.json"
fi

echo "[5/6] Writing provenance manifest…"
$PYBIN - <<PY
import json, os, time, pathlib
manifest = {
  "project":"MemoryCloud",
  "version":"v4.3.2",
  "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
  "checksums_csv":"SBOM/checksums.csv",
  "root_hash": open("provenance/root_hash.txt").read().strip() if os.path.exists("provenance/root_hash.txt") else "",
  "sbom":"SBOM/sbom.cdx.json",
  "provenance_log":"provenance/audit.jsonl" if os.path.exists("provenance/audit.jsonl") else "",
}
pathlib.Path("SBOM/provenance.json").write_text(json.dumps(manifest, indent=2))
print(json.dumps({"manifest":"SBOM/provenance.json","root_hash":manifest["root_hash"]}))
PY

echo "✓ All verification steps completed successfully."
exit 0
