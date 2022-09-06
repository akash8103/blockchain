import json
 
from web3 import Web3
 
# In the video, we forget to `install_solc`
# from solcx import compile_standard
from solcx import compile_standard, install_solc
import os
 
 
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
 
# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.6.0")
 
# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)
 
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
 
# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
 
# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]
 
# w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL")))
# chain_id = 4
#
# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xD0e3858FB0c9eB269803195E33D06439738Bcd8d"
private_key = "9c4206d3aeb9db9a2887db6a949273b1fa23073f69eb5de0271ba8458873871a"
 
# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# print(transaction)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
 
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
 
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(f"Done! Contract deployed to {tx_receipt.contractAddress}")
 
 
# # Working with deployed Contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")