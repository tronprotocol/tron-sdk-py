# tron-sdk-py

The TRON gRPC API SDK in Python.

## Demo

```py
from tron.proto.core.contract_pb2 import TransferContract
from tron.client import TronClient
from tron.types import HEX, ADDR

client = TronClient.nile(
    private_key=HEX('3333333333333333333333333333333333333333333333333333333333333333')
)


print(client.solidity_stub.GetNowBlock2(EmptyMessage()))


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
```
