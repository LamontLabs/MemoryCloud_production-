# ───────────────────────────────────────────────
# MemoryCloud™ — Makefile
# Version: v4.3
# Owner: Jesse J. Lamont • Org: Lamont Labs
# Date: 2025-10-05
# Purpose: Automate setup, demo runs, verification,
# and reproducibility for the deterministic demo.
# ───────────────────────────────────────────────

APP=src/memorycloud/main.py
VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

# Default environment file
ENV_FILE=.env

# ───────────────────────────────────────────────
# Setup & Environment
# ───────────────────────────────────────────────
setup:
	@echo "[+] Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "[+] Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "[+] Environment setup complete."

env-check:
	@test -f $(ENV_FILE) || (echo "[-] .env not found. Copying from .env.example..." && cp .env.example .env)

# ───────────────────────────────────────────────
# Run & Demo
# ───────────────────────────────────────────────
run: env-check
	@echo "[+] Starting MemoryCloud FastAPI demo..."
	$(PYTHON) -m uvicorn src.memorycloud.main:app --host 127.0.0.1 --port 8000 --reload

demo:
	@echo "[+] Running CLI demo (HUD)..."
	$(PYTHON) cli/mc_demo.py --seed data/demo_seed.json

# ───────────────────────────────────────────────
# Testing & QA
# ───────────────────────────────────────────────
test:
	@echo "[+] Running pytest suite..."
	$(PYTHON) -m pytest -v

lint:
	@echo "[+] Running flake8 lint..."
	flake8 src tests

typecheck:
	@echo "[+] Running mypy type checks..."
	mypy src/

# ───────────────────────────────────────────────
# Provenance & Verification
# ───────────────────────────────────────────────
verify:
	@echo "[+] Running deterministic verification..."
	bash verify.sh

sbom:
	@echo "[+] Generating CycloneDX SBOM..."
	$(PYTHON) -m cyclonedx_py -r requirements.txt -o SBOM/sbom.cdx.json
	@echo "[+] SBOM generated → SBOM/sbom.cdx.json"

provenance:
	@echo "[+] Creating provenance manifest..."
	$(PYTHON) src/memorycloud/provenance.py --generate SBOM/provenance.json

# ───────────────────────────────────────────────
# Release & Packaging
# ───────────────────────────────────────────────
release:
	@echo "[+] Building release bundle..."
	mkdir -p dist
	tar -czf dist/MemoryCloud_v4.3_demo.tar.gz src/ docs/ SBOM/ LICENSE README.md
	@echo "[+] Release created → dist/MemoryCloud_v4.3_demo.tar.gz"

clean:
	@echo "[+] Cleaning workspace..."
	rm -rf $(VENV) __pycache__/ .mypy_cache/ .pytest_cache/ dist/ logs/
	@echo "[+] Done."

# ───────────────────────────────────────────────
# Help
# ───────────────────────────────────────────────
help:
	@echo "MemoryCloud™ Makefile Commands"
	@echo "  make setup         - Setup environment"
	@echo "  make run           - Run FastAPI app"
	@echo "  make demo          - Run CLI demo"
	@echo "  make test          - Run pytest suite"
	@echo "  make verify        - Run deterministic checks"
	@echo "  make sbom          - Generate CycloneDX SBOM"
	@echo "  make release       - Package release bundle"
	@echo "  make clean         - Clean repo artifacts"

# End of file
