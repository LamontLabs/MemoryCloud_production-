from fastapi import APIRouter, HTTPException
from src.memorycloud.crypto import seal_data
from src.memorycloud.store import insert_memory
from src.memorycloud.provenance import append_event
from src.memorycloud.hud import render_hud

router = APIRouter()

@router.post("/capture")
async def capture_route(payload: dict):
    text = payload.get("text")
    indicator = bool(payload.get("indicator", False))
    if not text:
        raise HTTPException(status_code=400, detail="Missing text")
    if not indicator:
        append_event("capture_reject", {"reason": "indicator_off"})
        return {"stored": False, "hud": "✖"}
    encrypted = seal_data(text.encode())
    insert_memory(text, indicator, encrypted)
    append_event("capture", {"text": text})
    return {"stored": True, "hud": render_hud(True)}
