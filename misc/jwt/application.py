import datetime
import os

import jwt

# Decode algorithms.
# Examples: ['RS256', 'RS384', 'RS512', 'ES256', 'ES384', 'ES521', 'ES512', 'PS256', 'PS384', 'PS512']
DECODE_ALGORITHMS = []


def encode(application_key, application_secret):
    iat = datetime.datetime.utcnow()
    return jwt.encode(
        {
            'iss': application_key,
            'iat': iat,
            'jti': generate_nonce(),
        },
        application_secret,
    ).decode()


def decode(access_token, secret=None, verify=True):
    try:
        if verify:
            token = jwt.decode(access_token, secret, algorithms=DECODE_ALGORITHMS)
        else:
            token = jwt.decode(access_token, verify=False, algorithms=DECODE_ALGORITHMS)
    except jwt.InvalidTokenError:
        return None
    return token


def generate_nonce():
    """
    Generate jti, it is a unique identified that is used to prevent the JWT from being replayed.
    """
    return os.urandom(4).hex()
