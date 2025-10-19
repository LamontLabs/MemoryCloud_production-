# ───────────────────────────────────────────────
# MemoryCloud™ — Makefile  [REPLACEMENT]
# Version: v4.3  •  Date: 2025-10-05
# Fixes:
#  - Force Python 3.11 everywhere
#  - Upgrade pip/setuptools/wheel before install
#  - Correct CycloneDX command
# ───────────────────────────────────────────────

PY := python3.11
VENV := .venv
PIP := $(VENV)/bin/pip
PYBIN := $(VENV)/bin/python

APP=src/memorycloud/main.py

.DEFAULT_GOAL := help

setup:
	@echo "[+] Creating virtualenv with Python 3.11"
	$(PY) -m venv $(VENV)
	@echo "[+] Upgrading build tooling"
	$(PYBIN) -m pip install --upgrade pip setuptools wheel
	@echo "[+] Installing pinned requirements"
	$(PIP) install -r requirements.txt
	@echo "[✓] Setup complete"

run:
	@echo "[+] Starting FastAPI on http://127.0.0.1:8000"
	$(PYBIN) -m uvicorn src.memorycloud.main:app --host 127.0.0.1 --port 8000 --reload

demo:
	@echo "[i] Minimal demo: use curl to POST /capture then GET /recall"

test:
	@echo "[+] Running tests"
	$(PYBIN) -m pytest -v

lint:
	@echo "[+] Lint (non-fatal)"
	$(VENV)/bin/flake8 src tests || true
	$(VENV)/bin/black --check src tests || { echo "[!] Formatting with black" ; $(VENV)/bin/black src tests ; }

typecheck:
	@echo "[+] Typecheck (non-fatal)"
	$(VENV)/bin/mypy src || true

verify:
	@echo "[+] Verifying determinism & provenance"
	bash verify.sh

sbom:
	@echo "[+] Generating CycloneDX SBOM"
	$(VENV)/bin/cyclonedx-bom -o SBOM/sbom.cdx.json -e requirements.txt
	@echo "[✓] SBOM → SBOM/sbom.cdx.json"

release:
	@echo "[+] Building demo bundle"
	mkdir -p dist
	tar -czf dist/MemoryCloud_v4.3_demo.tar.gz \
		README.md INSTALL.md OPERATIONS.md CONFIG.md LIMITATIONS.md HANDOFF.md ROADMAP.md LICENSE \
		requirements.txt Makefile verify.sh manifest.json PROVENANCE.md SECURITY.md PRIVACY.md CHANGELOG.md \
		src tests data migrations SBOM assets .github
	@echo "[✓] dist/MemoryCloud_v4.3_demo.tar.gz"

clean:
	@echo "[+] Cleaning workspace"
	rm -rf $(VENV) __pycache__ .pytest_cache .mypy_cache dist logs provenance/root_hash.txt
	@echo "[✓] Clean"

help:
	@echo "MemoryCloud™ Make Targets"
	@echo "  make setup     - create venv + install deps (py3.11)"
	@echo "  make run       - run FastAPI with reload"
	@echo "  make test      - run pytest"
	@echo "  make verify    - determinism + provenance checks"
	@echo "  make sbom      - generate CycloneDX SBOM"
	@echo "  make release   - package demo bundle"
	@echo "  make clean     - remove build artifacts"
