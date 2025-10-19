from pydantic import BaseModel, Field
from datetime import datetime

class CaptureRequest(BaseModel):
    text: str = Field(..., description="Captured memory text")
    indicator: bool = Field(..., description="Indicator ON/OFF")

class RecallResponse(BaseModel):
    id: int
    text: str
    indicator: bool
    created_at: datetime

class AuditRecord(BaseModel):
    ts: str
    action: str
    payload_hash: str
    prev_hash: str
    hash: str
