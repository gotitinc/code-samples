import os
import random
import re

from Crypto.Hash import SHA512
from flask import request


def get_client_ip_address():
    """
    Get ip address of the requested client
    :return:
    """
    # Check for proxy first
    if request.headers.getlist('X-Forwarded-For'):
        return request.headers.getlist('X-Forwarded-For')[0]
    else:
        return request.remote_addr


def generate_salt(length, encode='ascii'):
    return os.urandom(length).encode(encode)


def generate_hash(str, salt):
    h = SHA512.new()
    try:
        h.update(salt)
        h.update(str)
    except UnicodeEncodeError:
        raise ValueError
    digest = h.hexdigest()
    return digest


def generate_random_string(length, sequence='abcdef'):
    return ''.join(random.sample(sequence, length))


def is_empty(text: str) -> bool:
    if text == '':
        return True
    return False


def contains_whitespace(text: str) -> bool:
    if re.search(r"\s", text):
        return True
    return False


def has_length_less_than(text: str, length: int) -> bool:
    if len(text) < length:
        return True
    return False


def has_at_least_1_digit(text: str) -> bool:
    if re.search(r"\d", text) is None:
        return False
    return True


def has_at_least_1_uppercase(text: str) -> bool:
    if re.search(r"[A-Z]", text) is None:
        return False
    return True


def has_at_least_1_lowercase(text: str) -> bool:
    if re.search(r"[a-z]", text) is None:
        return False
    return True
