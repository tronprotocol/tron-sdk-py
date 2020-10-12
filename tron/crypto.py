from Crypto.Hash import keccak
import hashlib


def keccak256(data: bytes) -> bytes:
    hasher = keccak.new(digest_bits=256)
    hasher.update(data)
    return hasher.digest()


def sha256(data: bytes) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.digest()