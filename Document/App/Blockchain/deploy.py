from solcx import compile_standard, install_solc
import json
from web3 import Web3

install_solc("0.8.0")

with open("Blockchain/contracts/FileStorage.sol", "r") as file:
    file_storage = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"FileStorage.sol": {"content": file_storage}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

bytecode = compiled_sol["contracts"]["FileStorage.sol"]["FileStorage"]["evm"]["bytecode"]["object"]

abi = compiled_sol["contracts"]["FileStorage.sol"]["FileStorage"]["abi"]

with open("Blockchain/abi.json", "w") as f:
    json.dump(abi, f)

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

chain_id = 1337
my_address = "0xFb5Be16e1bd9e9b6fe64A58175da788170d83b29"
private_key = "0x10580e516a27e90f63dfa2e550d6509213c03c346bfbf536ae0c881812bb352e"

FileStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.get_transaction_count(my_address)

transaction = FileStorage.constructor().build_transaction({
    "chainId": chain_id,
    "gas": 2000000,
    "gasPrice": w3.to_wei("50", "gwei"),
    "nonce": nonce,
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract Deployed At:", tx_receipt.contractAddress)