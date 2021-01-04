import os
import random

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
