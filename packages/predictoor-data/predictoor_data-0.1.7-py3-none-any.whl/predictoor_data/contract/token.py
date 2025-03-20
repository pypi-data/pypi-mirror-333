from predictoor_data.contract.base_contract import BaseContract
from predictoor_data.util.currency_types import Wei
from web3.types import TxParams, Wei as Web3Wei

from predictoor_data.w3_config.w3_config import Web3Config

class Token(BaseContract):
    def __init__(self, web3_config: Web3Config, address: str):
        super().__init__(web3_config, address, "ERC20Template3")

    def allowance(self, account, spender) -> Wei:
        return Wei(self.contract_instance.functions.allowance(account, spender).call())

    def balanceOf(self, account) -> Wei:
        return Wei(self.contract_instance.functions.balanceOf(account).call())

    def transfer(self, to: str, amount: Wei, sender, wait_for_receipt=True):
        gas_price = self.web3_pp.tx_gas_price()
        call_params = {"from": sender, "gasPrice": gas_price}
        tx = self.contract_instance.functions.transfer(
            to, int(amount.amt_wei)
        ).transact(call_params)
        if not wait_for_receipt:
            return tx
        return self.config.w3.eth.wait_for_transaction_receipt(tx)

    def approve(self, spender, amount: Wei, wait_for_receipt=True):
        call_params = self.web3_config.tx_call_params()
        # print(f"Approving {amount} for {spender} on contract {self.contract_address}")
        tx = self.contract_instance.functions.approve(spender, amount.amt_wei).transact(
            call_params
        )

        if not wait_for_receipt:
            return tx

        return self.config.w3.eth.wait_for_transaction_receipt(tx)


class NativeToken:
    def __init__(self, web3_pp):
        self.web3_pp = web3_pp

    @property
    def w3(self):
        return self.web3_pp.web3_config.w3

    @property
    def name(self):
        return "ROSE"

    def balanceOf(self, account) -> Wei:
        return Wei(self.w3.eth.get_balance(account))

    def transfer(self, to: str, amount: Wei, sender, wait_for_receipt=True):
        gas_price = self.web3_pp.tx_gas_price()
        call_params: TxParams = {
            "from": sender,
            "gas": 25000,
            "value": Web3Wei(int(amount.amt_wei)),
            "gasPrice": gas_price,
            "to": to,
        }
        tx = self.w3.eth.send_transaction(transaction=call_params)

        if not wait_for_receipt:
            return tx
        return self.w3.eth.wait_for_transaction_receipt(tx)