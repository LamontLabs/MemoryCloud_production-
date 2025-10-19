from src.memorycloud.crypto import seal_data, unseal_data

def test_seal_unseal_cycle():
    original = b"memorycloud_test_payload"
    encrypted = seal_data(original)
    decrypted = unseal_data(encrypted)
    assert decrypted == original
