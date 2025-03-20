import os
import time
from typing import Optional

from eth_typing import BlockIdentifier
from predictoor_data.constants import RPC_URL

from eth_keys import KeyAPI
from eth_keys.backends import NativeECCBackend

from web3 import Web3
from web3.middleware import (
    construct_sign_and_send_raw_middleware,
    http_retry_request_middleware
)
from web3.types import BlockData


_KEYS = KeyAPI(NativeECCBackend)

class Web3Config:
    def __init__(self, private_key: Optional[str]):
        self.private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider(_get_rpc_url()))
        self.account = self.w3.eth.account.from_key(private_key)
        self.owner = self.account.address
        self.w3.middleware_onion.add(construct_sign_and_send_raw_middleware(self.account))
        self.w3.middleware_onion.add(http_retry_request_middleware)


    def get_block(
        self, block: BlockIdentifier, full_transactions: bool = False, tries: int = 0
    ) -> BlockData:
        try:
            block_data = self.w3.eth.get_block(block)
            return block_data
        except Exception as e:
            if tries < 5:
                time.sleep(((tries + 1) / 2) ** (2) * 10)
                return self.get_block(block, full_transactions, tries + 1)
            raise Exception("Couldn't get block") from e

    def tx_gas_price(self) -> int:
        """Return gas price for use in call_params of transaction calls."""
        return self.w3.eth.gas_price

    def tx_call_params(self, gas=None) -> dict:
        call_params = {
            "from": self.owner,
            "gasPrice": self.tx_gas_price(),
        }
        if gas is not None:
            call_params["gas"] = gas
        return call_params

    def get_auth_signature(self):
        """
        @description
          Digitally sign

        @return
          auth -- dict with keys "userAddress", "v", "r", "s", "validUntil"
        """
        valid_until = self.get_block("latest").timestamp + 3600
        message_hash = self.w3.solidity_keccak(
            ["address", "uint256"],
            [self.owner, valid_until],
        )
        pk = _KEYS.PrivateKey(self.account.key)
        prefix = "\x19Ethereum Signed Message:\n32"
        signable_hash = self.w3.solidity_keccak(
            ["bytes", "bytes"],
            [
                self.w3.to_bytes(text=prefix),
                self.w3.to_bytes(message_hash),
            ],
        )
        signed = _KEYS.ecdsa_sign(message_hash=signable_hash, private_key=pk)
        auth = {
            "userAddress": self.owner,
            "v": (signed.v + 27) if signed.v <= 1 else signed.v,
            "r": self.w3.to_hex(self.w3.to_bytes(signed.r).rjust(32, b"\0")),
            "s": self.w3.to_hex(self.w3.to_bytes(signed.s).rjust(32, b"\0")),
            "validUntil": valid_until,
        }
        return auth

def _get_rpc_url() -> str:
    """
    if env PREDICTOOR_RPC is set, return that, otherwise return default
    """
    return os.getenv("PREDICTOOR_RPC", RPC_URL)

def get_web3_config(private_key: Optional[str]):
    return Web3Config(private_key)



    
