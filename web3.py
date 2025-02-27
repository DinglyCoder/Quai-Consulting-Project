from web3 import Web3

# Connect to Ethereum network (e.g., Infura or local node)
w3 = Web3(Web3.HTTPProvider("https://your_rpc_url"))

# Contract details
contract_address = "0xYourContractAddress"
contract_abi = [...]  # Load your contract's ABI
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Wallet setup
private_key = "your_private_key"
wallet_address = w3.to_checksum_address("0xYourWalletAddress")

# Read amounts and wallets from a file
recipients = [
    "0xRecipientAddress1",
    "0xRecipientAddress2",
]
amounts = [
    w3.to_wei(0.1, "ether"),
    w3.to_wei(0.2, "ether"),
]

# Build transaction
tx = contract.functions.distribute(recipients, amounts).build_transaction({
    "from": wallet_address,
    "value": sum(amounts),
    "gas": 300000,
    "gasPrice": w3.to_wei("50", "gwei"),
    "nonce": w3.eth.get_transaction_count(wallet_address),
})

# Sign and send transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("Transaction sent:", tx_hash.hex())