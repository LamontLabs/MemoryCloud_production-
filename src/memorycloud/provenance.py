import json
import hashlib
import os
from datetime import datetime
from src.memorycloud.config import settings

os.makedirs(os.path.dirname(settings.audit_log), exist_ok=True)

def append_event(action: str, payload: dict):
    record = {
        "ts": datetime.utcnow().isoformat(),
        "action": action,
        "payload_hash": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
        "prev_hash": _get_last_hash()
    }
    record["hash"] = hashlib.sha256(
        (record["ts"] + record["action"] + record["payload_hash"] + record["prev_hash"]).encode()
    ).hexdigest()

    with open(settings.audit_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return record["hash"]

def _get_last_hash():
    if not os.path.exists(settings.audit_log):
        return ""
    with open(settings.audit_log, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        return ""
    last = json.loads(lines[-1])
    return last.get("hash", "")
