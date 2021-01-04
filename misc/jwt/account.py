import datetime
import os

import jwt

JWT_SECRET = ''
LEEWAY = 5  # seconds
# Decode algorithms.
# Examples: ['RS256', 'RS384', 'RS512', 'ES256', 'ES384', 'ES521', 'ES512', 'PS256', 'PS384', 'PS512']
DECODE_ALGORITHMS = []
TOKEN_LIFETIME = 1


def encode(sub, nonce):
    iat = datetime.datetime.utcnow()
    return jwt.encode({
        'sub': sub,
        'iat': iat,
        'exp': iat + datetime.timedelta(days=TOKEN_LIFETIME),
        'nonce': nonce,
    }, JWT_SECRET).decode()


def decode(access_token, audience):
    try:
        token = jwt.decode(
            access_token, JWT_SECRET, leeway=LEEWAY, algorithms=DECODE_ALGORITHMS, audience=audience
        )
    except jwt.InvalidTokenError:
        return None
    return token


def generate_access_token_nonce():
    return os.urandom(4).hex()
