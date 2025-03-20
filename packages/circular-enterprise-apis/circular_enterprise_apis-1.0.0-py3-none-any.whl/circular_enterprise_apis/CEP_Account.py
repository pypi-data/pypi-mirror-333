import json
import hashlib
import time
import requests
from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.util import sigencode_der
from ecdsa.rfc6979 import generate_k
from . import helper


LIB_VERSION = helper.LIB_VERSION
DEFAULT_NAG = helper.DEFAULT_NAG
NETWORK_URL = helper.NETWORK_URL
DEFAULT_CHAIN = helper.DEFAULT_CHAIN

class CEP_Account:
    """
    Circular Account Class
    """

    def __init__(self):
        self.address = None
        self.publicKey = None
        self.info = None
        self.codeVersion = LIB_VERSION
        self.lastError = ''
        self.NAG_URL = DEFAULT_NAG
        self.NETWORK_NODE = ''
        self.blockchain = DEFAULT_CHAIN
        self.LatestTxID = ''
        self.Nonce = 0
        self.data = []
        self.intervalSec = 2

    def open(self, address):
        """
        Open an account by retrieving all the account info
        :param address: Account address
        :return: True if successful, False otherwise
        """
        if not address:
            self.lastError = "Invalid address"
            return False
        self.address = address
        return True

    def update_account(self):
        """
        Update the account data and Nonce field
        :return: True if successful, False otherwise
        """
        if not self.address:
            self.lastError = "Account not open"
            return False

        data = {
            "Blockchain": helper.hex_fix(self.blockchain),
            "Address": helper.hex_fix(self.address),
            "Version": self.codeVersion,
        }

        try:
            response = requests.post(self.NAG_URL + "Circular_GetWalletNonce_", json=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            response_data = response.json()

            if response_data['Result'] == 200 and 'Response' in response_data and 'Nonce' in response_data['Response']:
                self.Nonce = response_data['Response']['Nonce'] + 1
                return True
            else:
                self.lastError = "Invalid response format or missing Nonce field"
                return False

        except requests.exceptions.RequestException as e:
            self.lastError = f"Network error: {e}"
            return False
        except json.JSONDecodeError as e:
            self.lastError = f"Invalid JSON response: {e}"
            return False
        except KeyError:
            self.lastError = "Invalid response format"
            return False

    def set_network(self, network):
        """
        Set the blockchain network
        :param network: Network name (e.g., 'devnet', 'testnet', 'mainnet')
        :return: URL of the network
        :raises Exception: If network URL cannot be fetched
        """
        nag_url = NETWORK_URL + requests.utils.quote(network)

        try:
            response = requests.get(nag_url)
            response.raise_for_status()
            data = response.json()

            if 'status' in data and data['status'] == 'success' and 'url' in data:
                return data['url']
            else:
                raise Exception(data.get('message', 'Failed to get URL'))

        except requests.exceptions.RequestException as e:
            print(f'Error fetching network URL: {e}')
            raise e
        except json.JSONDecodeError as e:
            raise Exception(f'Failed to parse JSON: {e}')

    def set_blockchain(self, blockchain):
        """
        Set the blockchain address
        :param blockchain: Blockchain address
        """
        self.blockchain = blockchain

    def close(self):
        """
        Close the account
        """
        self.address = None
        self.publicKey = None
        self.info = None
        self.lastError = ''
        self.NAG_URL = None
        self.NETWORK_NODE = None
        self.blockchain = None
        self.LatestTxID = None
        self.data = None
        self.Nonce = 0
        self.intervalSec = 0

    def sign_data(self, data, private_key_hex, address):
        """
        Sign data using the account's private key
        :param data: Data to sign
        :param private_key_hex: Private key in hex format
        :param address: Account address
        :return: Signature in hex format
        :raises Exception: If account is not open
        """
        if not self.address:
            raise Exception("Account is not open")

        private_key = ecdsa.SigningKey.from_string(bytes.fromhex(helper.hex_fix(private_key_hex)), curve=ecdsa.SECP256k1)
        message_hash = hashlib.sha256(data.encode()).digest()
        signature = private_key.sign_digest(message_hash)
        return signature.hex()

    def get_transaction_by_id(self, tx_id, start, end):
        """
        Get transaction by ID
        """
        data = {
            "Blockchain": helper.hex_fix(self.blockchain),
            "ID": helper.hex_fix(tx_id),
            "Start": str(start),
            "End": str(end),
            "Version": self.codeVersion
        }
        url = self.NAG_URL + 'Circular_GetTransactionbyID_' + self.NETWORK_NODE
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {e}")

    def get_transaction(self, block_num, tx_id):
        """
        Search for a transaction by its ID
        """
        data = {
            "Blockchain": helper.hex_fix(self.blockchain),
            "ID": helper.hex_fix(tx_id),
            "Start": str(block_num),
            "End": str(block_num),
            "Version": self.codeVersion
        }
        url = self.NAG_URL + 'Circular_GetTransactionbyID_' + self.NETWORK_NODE
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            raise e
        except json.JSONDecodeError as e:
            raise Exception(f'Invalid JSON response: {e}')


    def get_transaction_outcome(self, TxID, timeoutSec, intervalSec=10):
        """
        Recursive transaction finality polling

        Args:
            Blockchain: Blockchain name
            TxID: Transaction ID
            intervalSec: Polling interval in seconds
            timeoutSec: Timeout in seconds

        Returns:
            Transaction outcome
        """

        def checkTransaction():
            elapsedTime = helper.datetime.now() - startTime
            print('Checking transaction...')

            if elapsedTime.total_seconds() > timeoutSec:
                print('Timeout exceeded')
                raise TimeoutError('Timeout exceeded')

            data = self.get_transaction_by_id(TxID, 0, 10)
            print('Data received:', data)
            if data['Result'] == 200 and data['Response'] != 'Transaction Not Found' and data['Response']['Status'] != 'Pending':
                return data
            else:
                print('Transaction not yet confirmed or not found, polling again...')
                time.sleep(intervalSec)
                return checkTransaction()

        startTime = helper.datetime.now()

        return checkTransaction()

    def sign_data(self, message, private_key):
        key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        msgHash = hashlib.sha256(message.encode()).digest()
        
        # Generate a deterministic k value (RFC 6979)
        k = generate_k(
            key.curve.order,                      # Order of the curve
            key.privkey.secret_multiplier,        # Private key multiplier 
            hash_func=hashlib.sha256,             # Hash function
            data=msgHash                          # Data to hash
        )
        # Sign the message using the private key and the deterministic k value
        signature = key.sign_digest(msgHash, sigencode=sigencode_der, k=k)
        return signature.hex()

    def submit_certificate(self, pdata, private_key_hex):
            if not self.address:
                raise Exception("Account is not open")

            payload_object = {
                "Action": "CP_CERTIFICATE",
                "Data": helper.string_to_hex(pdata)
            }
            json_str = json.dumps(payload_object)
            payload = helper.string_to_hex(json_str)
            timestamp = helper.get_formatted_timestamp()
            str_to_hash = helper.hex_fix(self.blockchain) + helper.hex_fix(self.address) + helper.hex_fix(self.address) + payload + str(self.Nonce) + timestamp
            tx_id = hashlib.sha256(str_to_hash.encode()).hexdigest()
            signature = self.sign_data(tx_id, private_key_hex)

            data = {
                "ID": tx_id,
                "From": helper.hex_fix(self.address),
                "To": helper.hex_fix(self.address),
                "Timestamp": timestamp,
                "Payload": payload,
                "Nonce": str(self.Nonce),
                "Signature": signature,
                "Blockchain": helper.hex_fix(self.blockchain),
                "Type": 'C_TYPE_CERTIFICATE',
                "Version": self.codeVersion
            }

            url = self.NAG_URL + 'Circular_AddTransaction_' + self.NETWORK_NODE
            try:
                response = requests.post(url, json=data)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                raise