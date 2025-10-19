from fastapi import APIRouter
from src.memorycloud.store import list_memories
from src.memorycloud.provenance import append_event

router = APIRouter()

@router.get("/recall")
async def recall_route(q: str | None = None):
    items = list_memories(q)
    append_event("recall", {"query": q})
    return {"matches": items}
