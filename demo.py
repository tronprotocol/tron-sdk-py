
import grpc

from tron.proto.api.api_pb2_grpc import WalletStub, WalletSolidityStub
from tron.proto.api.api_pb2 import EmptyMessage, AccountAddressMessage, BytesMessage
from tron.types import ADDR

channel = grpc.insecure_channel('grpc.trongrid.io:50051')
stub = WalletStub(channel)

solidity_stub = WalletStub(channel)


resp = solidity_stub.GetNowBlock2(EmptyMessage())
print(resp)

print('=' * 80)

"""
req = AccountAddressMessage()
req.address = bytes.fromhex("41adfd40f3d6575c4747f25c1bb03cf0bd415c142f")
resp = stub.GetAccount(req)
print(resp)
"""

req = AccountAddressMessage()
req.address = ADDR("TRqBHd4srhfHMnfCefdF6fnkR8f71BUUY1")
resp = stub.GetAccount(req)
print(resp)
