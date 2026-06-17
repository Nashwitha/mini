import json
from web3 import Web3

GANACHE_URL = "HTTP://127.0.0.1:7545"
CONTRACT_ADDRESS = "0x3bE0C518d625fBcd34685CB10c6A05CFb7AC4D81"

w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

with open("Blockchain/abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

account = w3.eth.accounts[0]


def store_file_hash(file_hash):

    tx = contract.functions.storeFile(file_hash).transact({
        'from': account
    })

    receipt = w3.eth.wait_for_transaction_receipt(tx)

    return receipt.transactionHash.hex()


def verify_file_hash(file_hash):

    result = contract.functions.verifyFile(file_hash).call()

    return result