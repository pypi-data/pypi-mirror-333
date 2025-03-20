import pytest
import requests
import json
import os
from circular_enterprise_apis import CEP_Account, helper  # Replace your_module

# Replace with your test values (keep private keys secure)
TEST_ADDRESS = os.environ.get("TEST_ADDRESS", "your-wallet-address")
TEST_PRIVATE_KEY = os.environ.get("TEST_PRIVATE_KEY", "your-private-key")
TEST_BLOCKCHAIN = "0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2"
TEST_NETWORK = os.environ.get("TEST_NETWORK", "testnet") # "testnet", or "devnet", or "mainnet"

@pytest.mark.integration
def test_integration_flow_api():
    account = CEP_Account()
    tx_id = None
    tx_block = None

    try:
        print("Opening Account")
        account.open(TEST_ADDRESS)
        account.set_blockchain(TEST_BLOCKCHAIN)
        account.set_network(TEST_NETWORK)
        print(account.NAG_URL)
        print(account.NETWORK_NODE)
        print("Updating Account")
        update_result = account.update_account()
        print("Account updated")
        assert update_result is True
        print("Account up to date")
        print("Nonce : ", account.Nonce)

        print("Submitting Transaction")
        submit_result = account.submit_certificate("test Enterprise APIs", TEST_PRIVATE_KEY)

        print("Result :", submit_result)
        assert submit_result["Result"] == 200
        print("Certificate submitted successfully:", submit_result)
        tx_id = submit_result["Response"]["TxID"]

        print("Getting Transaction Outcome")
        outcome = account.get_transaction_outcome(tx_id, 25) # Using get_transaction_by_id to simulate GetTransactionOutcome
        print("Report ", outcome)
        print(json.dumps(outcome))

        assert outcome["Response"]["Status"] == "Executed" and outcome["Result"] == 200
        tx_block = outcome["Response"]["BlockID"]
        print("Transaction ID:", tx_id)
        print("Transaction Block:", tx_block)

        print("Searching Transaction")
        get_tx_result = account.get_transaction(tx_block, tx_id)
        print("Get Transaction Result :", get_tx_result)

        assert get_tx_result["Result"] == 200
        print("Certificate found :", get_tx_result)

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Network error: {e}")
    except json.JSONDecodeError as e:
        pytest.fail(f"Invalid JSON response: {e}")
    except KeyError:
        pytest.fail(f"Invalid response format")
    except Exception as error:
        print(f"An error occurred: {error}")
        pytest.fail(f"An error occurred: {error}")
    finally:
        account.close()
        print("Account Closed")


test_integration_flow_api()