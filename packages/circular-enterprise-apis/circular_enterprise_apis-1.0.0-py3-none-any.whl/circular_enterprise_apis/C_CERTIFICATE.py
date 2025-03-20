import json
from . import helper


LIB_VERSION = helper.LIB_VERSION

class C_CERTIFICATE:
    """
    Circular Certificate Class for certificate chaining
    """

    def __init__(self):
        self.data = None
        self.previousTxID = None
        self.previousBlock = None

    def set_data(self, data):
        """
        Insert application data into the certificate
        :param data: Data content
        """
        self.data = helper.string_to_hex(data)

    def get_data(self):
        """
        Extract application data from the certificate
        :return: Data content
        """
        return helper.hex_to_string(self.data)

    def get_json_certificate(self):
        """
        Get the certificate in JSON format
        :return: JSON-encoded certificate
        """
        certificate = {
            "data": self.get_data(),
            "previousTxID": self.previousTxID,
            "previousBlock": self.previousBlock,
            "version": LIB_VERSION
        }
        return json.dumps(certificate)

    def get_certificate_size(self):
        """
        Get the size of the certificate in bytes
        :return: Size of the certificate
        """
        return len(self.get_json_certificate().encode('utf-8'))