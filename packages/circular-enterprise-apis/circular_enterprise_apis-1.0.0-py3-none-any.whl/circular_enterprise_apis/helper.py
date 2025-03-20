"""
CIRCULAR Enterprise APIs for Data Certification

License : Open Source for private and commercial use

CIRCULAR GLOBAL LEDGERS, INC. - USA

Version : 1.0.0

Creation: 13/3/2025
Update  : 13/3/2025

Originator: Gianluca De Novi, PhD
Contributors: Danny De Novi
"""

import binascii
from datetime import datetime, timezone

# Global Constants
LIB_VERSION = '1.0.13'
NETWORK_URL = 'https://circularlabs.io/network/getNAG?network='
DEFAULT_CHAIN = '0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2'
DEFAULT_NAG = 'https://nag.circularlabs.io/NAG.php?cep='

# HELPER FUNCTIONS

def pad_number(num: int) -> str:
    """
    Function to add a leading zero to numbers less than 10
    :param num: Number to pad
    :return: Padded number
    """
    return f'0{num}' if num < 10 else str(num)

def get_formatted_timestamp() -> str:
    """
    Function to get the current timestamp in the format YYYY:MM:DD-HH:MM:SS
    :return: Formatted timestamp
    """
    now_utc = datetime.now(timezone.utc)
    return now_utc.strftime('%Y:%m:%d-%H:%M:%S')

def hex_fix(hex_str: str) -> str:
    """
    Removes '0x' from hexadecimal numbers if they have it
    :param hex_str: Hexadecimal string
    :return: Cleaned hexadecimal string
    """
    return hex_str.replace('0x', '')

def string_to_hex(string: str) -> str:
    """
    Convert a string to its hexadecimal representation without '0x'
    :param string: Input string
    :return: Hexadecimal representation
    """
    return hex_fix(binascii.hexlify(string.encode()).decode())

def hex_to_string(hex_str: str) -> str:
    """
    Convert a hexadecimal string to a regular string
    :param hex_str: Hexadecimal string
    :return: Regular string
    """
    return binascii.unhexlify(hex_str).decode()