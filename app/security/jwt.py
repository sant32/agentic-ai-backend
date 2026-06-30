import os 
import secrets
from datetime import datetime, timedelta, UTC
import jwt
from jwt import ExpiredSignatureError
from jwt import InvalidTokenError
import hashlib

SCERET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(user_id: int):

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.now(UTC) + timedelta(minutes=15),
        "iat": datetime.now(UTC)
    }

    return jwt.encode(payload, SCERET_KEY, ALGORITHM)


def create_refresh_token(user_id: int):

    jti = secrets.token_hex(16)

    payload = {
        "sub": str(user_id),
        "jti": jti,
        "type": "refresh",
        "exp": datetime.now(UTC)+ timedelta(days=7),
        "iat": datetime.now(UTC),
    }

    token = jwt.encode(
        payload,
        SCERET_KEY,
        ALGORITHM,
    )

    return token, jti





def decode_token(token: str):

    try:

        return jwt.decode(
            token,
            SCERET_KEY,
            ALGORITHM,
        )

    except ExpiredSignatureError:
        return None

    except InvalidTokenError:
        return None
    

def hash_refresh_token(token: str):

    return hashlib.sha256(
        token.encode()
    ).hexdigest()