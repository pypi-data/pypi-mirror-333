# Circular Enterprise Python APIs for Data Certification

This library provides Python implementations of the Circular Enterprise APIs
for data certification and blockchain integration. It includes classes and
helper functions to interact with the Circular network, submit certificates,
retrieve transactions, and manage accounts.

Features:
- Data Certification: Submit data to the blockchain for certification.
- Transaction Retrieval: Fetch transaction details by ID or block range.
- Account Management: Open, update, and close accounts.
- Secure Signing: Sign data using elliptic curve cryptography (secp256k1).
- Network Integration: Connect to different blockchain networks (mainnet, testnet, devnet).
"""

# Installation Instructions:

Installation

You can install this library using pip:

```sh
pip install circular_enterprise_apis
```

# Usage Instructions:

Usage

1. Opening an Account:
```python

from circular_enterprise_apis import CEP_Account

account = CEP_Account()
account.open('a4fc8b11bfc5dc2911ab41871e6de81f500fe60f3961343b202ad78e7e297ea08')

print("Account opened successfully.")
```
2. Choosing a network and the blockchain:
```python

blockchain = 'blockchain-address'
account.set_network("testnet") # chose between multiple networks such as testnet, devnet and mainnet
account.set_blockchain(blockchain)
```
3. Retrieve account informations
```python

if account.update_account():
    #...
```
4. Submitting a Certificate:
```python

pdata = 'Your data to certify'
private_key = 'your_private_key_here'

try:
    response = account.submit_certificate(pdata, private_key)
    print(response)
except Exception as e:
    print(f"Error: {e}")
```
5. Retrieving a Transaction:
```python

#...
resp = account.get_transaction_by_id(tx_id, 0, 10)
if resp["Response"]["BlockID"]:
    block_id = resp["Response"]["BlockID"]
    status = account.get_transaction(block_id, tx_id)

    if status["Result"] == 200:
        print(f"Transaction Status: {status['Response']['Status']}")
        account.close()
    else:
        print("Error on retrieving transaction")
else:
    print("Error on retrieving transaction status")
#...
```
Example Workflow:
```python
from circular_enterprise_apis import CEP_Account

try:
    # Instantiate the CEP Account class
    account = CEP_Account()
    print("CEP_Account instantiated successfully.")

    address = "your-account-address"
    private_key = "your-private-key"
    blockchain = "blockchain-address"
    tx_id = ""
    tx_block = ""

    account.set_network("testnet")
    account.set_blockchain(blockchain)
    print("Test variables set.")

    if account.open(address):
        print("Account opened successfully.")

        if account.update_account():
            print(f"Nonce: {account.Nonce}")

            tx_id_temp = account.submit_certificate(
                "your-data-to-certificate",
                private_key
            )
            if tx_id_temp["Result"] == 200:
                tx_id = tx_id_temp["Response"]["TxID"]
                print(f"TxID: {tx_id}")

                resp = account.get_transaction_by_id(tx_id, 0, 10)
                if resp["Response"]["BlockID"]:
                    block_id = resp["Response"]["BlockID"]
                    status = account.get_transaction(block_id, tx_id)

                    if status["Result"] == 200:
                        print(f"Transaction Status: {status['Response']['Status']}")
                        account.close()
                    else:
                        print("Error on retrieving transaction")
                else:
                    print("Error on retrieving transaction status")
            else:
                print("Certificate submission error")
        else:
            print(f"Update Account Error: {account.lastError}")
    else:
        print(f"Failed to open account: {account.lastError}")
except Exception as e:
    print(f"An error occurred: {e}")

```

# Helper Functions:

Helper Functions:
- hex_fix(hex): Removes '0x' from hexadecimal strings.
- string_to_hex(string): Converts a string to its hexadecimal representation.
- hex_to_string(hex): Converts a hexadecimal string back to a regular string.
- get_formatted_timestamp(): Returns the current timestamp in YYYY:MM:DD-HH:MM:SS format.


# Contributing:


Contributing:
Contributions are welcome! If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

# License:

License:
This project is licensed under the MIT License. See the LICENSE file for details.

# Support:

Support:
For questions or issues, please open an issue on the GitHub repository.
