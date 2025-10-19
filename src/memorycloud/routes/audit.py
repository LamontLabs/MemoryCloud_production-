import json
import os
from fastapi import APIRouter, HTTPException
from src.memorycloud.config import settings

router = APIRouter()

@router.get("/audit/export")
async def export_audit_route():
    if not os.path.exists(settings.audit_log):
        raise HTTPException(status_code=404, detail="No audit log found")
    with open(settings.audit_log, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]
    return {"records": lines, "count": len(lines)}
