from abc import ABC
import json


from predictoor_data.w3_config.w3_config import Web3Config
import pathlib

class BaseContract(ABC):
    def __init__(self, web3_config:Web3Config, address: str, contract_name: str):
        super().__init__()
        self.web3_config = web3_config
        current_dir = pathlib.Path(__file__).parent
        abi_path = current_dir / ".." / "abis" / f"{contract_name}.json"
        with open(abi_path) as f:
            abi = json.load(f)
        self.contract_address = self.config.w3.to_checksum_address(address)
        self.contract_instance = self.config.w3.eth.contract(
            address=self.config.w3.to_checksum_address(address),
            abi=abi,
        )
        self.contract_name = contract_name

    @property
    def config(self):
        return self.web3_config

    @property
    def name(self):
        return self.contract_name
