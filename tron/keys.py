import ecdsa  # type: ignore
from Crypto.Hash import keccak
import hashlib
import base58
import random

from tron.types import HEX, ADDR
from tron.crypto import keccak256


def sign_message(private_key: bytes, message: bytes) -> HEX:
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    public_key = sk.get_verifying_key().to_string()

    signature = sk.sign_deterministic(message)
    # recover address to get rec_id
    vks = ecdsa.VerifyingKey.from_public_key_recovery(
        signature, message, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256
    )

    for v, pk in enumerate(vks):
        if pk.to_string() == public_key:
            break

    signature += bytes([v])
    return HEX(signature)


def sign_message_hash(private_key: bytes, message_hash: bytes) -> HEX:
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    public_key = sk.get_verifying_key().to_string()

    signature = sk.sign_digest_deterministic(message_hash)
    # recover address to get rec_id
    vks = ecdsa.VerifyingKey.from_public_key_recovery_with_digest(
        signature, message_hash, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256
    )
    for v, pk in enumerate(vks):
        if pk.to_string() == public_key:
            break

    signature += bytes([v])
    return HEX(signature)


def private_key_to_address(private_key: bytes) -> ADDR:
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    public_key = sk.get_verifying_key().to_string()

    addr = b"\x41" + keccak256(public_key)[-20:]
    return ADDR(addr)


def recover_address_from_message(signature: bytes, message: bytes) -> ADDR:
    vks = ecdsa.VerifyingKey.from_public_key_recovery(
        signature[:64], message, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256
    )
    pub_key = vks[signature[-1]].to_string()
    addr = b"\x41" + keccak256(pub_key)[-20:]
    return ADDR(addr)


def recover_address_from_message_hash(signature: bytes, message_hash: bytes) -> ADDR:
    vks = ecdsa.VerifyingKey.from_public_key_recovery_with_digest(
        signature[:64], message_hash, curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256
    )
    pub_key = vks[signature[-1]].to_string()
    addr = b"\x41" + keccak256(pub_key)[-20:]
    return ADDR(addr)


if __name__ == "__main__":
    print(
        sign_message(
            HEX('e07fffdfe81c2c91c456aa4edf5f0b3a01701270c197b82b94b086a5d4b34484'),
            HEX("0000000000000000000000000d534491c956086e85f2f5aafcca9c44496d4e67"),
        )
    )

    print(
        recover_address_from_message(
            HEX(
                'aa53320b88b05aee306a115ed7fa994775a240ca207af7d740e1ac274633cdf72a73a36fe41cffca48dddfc7a5ff553a5c0305f106a291d34f5fdcd7cbefc72e01'
            ),
            HEX('0000000000000000000000000d534491c956086e85f2f5aafcca9c44496d4e67'),
        )
    )
