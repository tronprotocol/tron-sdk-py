from typing import Union
import grpc

from tron.proto.api.api_pb2_grpc import WalletStub, WalletSolidityStub
from tron.proto.api.api_pb2 import EmptyMessage, AccountAddressMessage, BytesMessage

from tron.proto.core.chain_pb2 import Transaction
from tron.proto.core.response_pb2 import TransactionExtention

from tron.types import ADDR, HEX
from tron.keys import private_key_to_address, sign_message


class TronClient(object):
    def __init__(self, private_key=None, endpoint="grpc.trongrid.io:50051"):
        channel = grpc.insecure_channel(endpoint)
        self.wallet_stub = WalletStub(channel)
        self.solidity_stub = WalletSolidityStub(channel)

        self.private_key = private_key
        self.address = None

        if self.private_key:
            self.address = private_key_to_address(self.private_key)

    def sign(self, txn: Union[Transaction, TransactionExtention]) -> Transaction:
        if not self.private_key:
            raise ValueError("private key is not set")
        if isinstance(txn, TransactionExtention):
            txn = txn.transaction

        msg = txn.raw_data.SerializeToString()
        signature = sign_message(self.private_key, msg)
        txn.signature.append(signature)

        return txn


if __name__ == "__main__":
    from tron.proto.core.contract_pb2 import TransferContract

    client = TronClient(
        endpoint="47.252.3.238:50051",
        private_key=HEX('3333333333333333333333333333333333333333333333333333333333333333'),
    )
    req = TransferContract()
    req.owner_address = ADDR("TJRabPrwbZy45sbavfcjinPJC18kjpRTv8")
    req.to_address = ADDR("TRsbuxREXKJKonexpejWhacE4sYHt1BSHV")
    req.amount = 1_100_000
    txn = client.wallet_stub.CreateTransaction2(req)

    print("TXID:", HEX(txn.txid))

    signed_txn = client.sign(txn)

    print(signed_txn)

    resp = client.wallet_stub.BroadcastTransaction(signed_txn)

    print(resp)
