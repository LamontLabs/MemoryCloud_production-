import json
from src.memorycloud.provenance import append_event, _get_last_hash

def test_audit_chain_integrity(tmp_path):
    log_path = tmp_path / "audit.jsonl"
    import src.memorycloud.config as config
    config.settings.audit_log = str(log_path)

    first = append_event("test_action", {"foo": "bar"})
    second = append_event("test_action_2", {"baz": "qux"})
    assert first != second
    last_hash = _get_last_hash()
    assert last_hash == second
    with open(log_path, "r", encoding="utf-8") as f:
        lines = [json.loads(l) for l in f]
    assert len(lines) == 2
