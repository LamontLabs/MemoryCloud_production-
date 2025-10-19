"""
Crypto subsystem — PyNaCl sealed-box & Ed25519 signing
"""

import os
import nacl.utils
from nacl.public import PrivateKey, SealedBox
from nacl.signing import SigningKey, VerifyKey

KEY_DIR = ".keys"
os.makedirs(KEY_DIR, exist_ok=True)

PRIVATE_KEY_PATH = os.path.join(KEY_DIR, "memorycloud.key")
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, "memorycloud.pub")

def _ensure_keys():
    if not os.path.exists(PRIVATE_KEY_PATH):
        sk = PrivateKey.generate()
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(sk.encode())
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(sk.public_key.encode())

def get_keys():
    _ensure_keys()
    sk = PrivateKey(open(PRIVATE_KEY_PATH, "rb").read())
    pk = sk.public_key
    return sk, pk

def seal_data(data: bytes) -> bytes:
    _, pk = get_keys()
    box = SealedBox(pk)
    return box.encrypt(data)

def unseal_data(data: bytes) -> bytes:
    sk, _ = get_keys()
    box = SealedBox(sk)
    return box.decrypt(data)

def sign_data(data: bytes) -> bytes:
    sign_key = SigningKey.generate()
    return sign_key.sign(data).signature

def verify_signature(data: bytes, sig: bytes, pubkey: bytes) -> bool:
    try:
        vk = VerifyKey(pubkey)
        vk.verify(data, sig)
        return True
    except Exception:
        return False
