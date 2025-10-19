from fastapi import FastAPI, HTTPException, Request
from src.memorycloud.store import init_db, insert_memory, list_memories
from src.memorycloud.crypto import seal_data
from src.memorycloud.provenance import append_event
from src.memorycloud.config import settings
from src.memorycloud.hud import render_hud

app = FastAPI(title=settings.app_name, version="4.3.0")

@app.on_event("startup")
def startup_event():
    init_db()
    append_event("startup", {"status": "ok"})

@app.post("/capture")
async def capture_memory(req: Request):
    body = await req.json()
    text = body.get("text")
    indicator = bool(body.get("indicator", False))
    if not text:
        raise HTTPException(status_code=400, detail="Missing text field")
    if settings.indicator_required and not indicator:
        append_event("capture_reject", {"reason": "indicator_off"})
        raise HTTPException(status_code=403, detail="Indicator required (fail-closed)")

    encrypted = seal_data(text.encode())
    insert_memory(text, indicator, encrypted)
    append_event("capture", {"text": text, "indicator": indicator})
    hud = render_hud(True)
    return {"stored": True, "hud": hud}

@app.get("/recall")
async def recall_memory(q: str | None = None):
    items = list_memories(q)
    append_event("recall", {"query": q, "count": len(items)})
    return {"matches": items}

@app.get("/audit/export")
async def export_audit():
    try:
        with open(settings.audit_log, "r", encoding="utf-8") as f:
            data = f.read().splitlines()
        return {"audit": [json.loads(line) for line in data if line.strip()]}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No audit log found")

@app.get("/health")
async def health():
    return {"status": "ok", "uptime": True}

@app.get("/ready")
async def ready():
    return {"ready": True, "env": settings.env}
