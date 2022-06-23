import base64
from datetime import datetime, timedelta
from typing import Any, Dict
from decouple import config
import json
import uuid

import jwt
from jwt.algorithms import ECAlgorithm


def prepare_key():
    algo = ECAlgorithm("ES256")
    key = config("ES256_KEY")
    decoded = base64.b64decode(key)
    json_key = json.loads(decoded)
    return algo.from_jwk(json_key.get("keys")[0])


def encode(sub: str):
    payload = {
        "iss": config("JWT_ISSUER"),
        "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
        "iat": datetime.utcnow(),
        "nbf": datetime.utcnow(),
        "sub": sub,
        "jit": str(uuid.uuid4()),
    }

    return payload, jwt.encode(
        payload,
        prepare_key(),
        algorithm=config("JWT_ALGO"),
        headers={"kid": config("ES256_KID")},
    )


def decode(encoded: str) -> Dict[str, Any]:
    try:
        pk = prepare_key().public_key()
        return jwt.decode(encoded, pk, algorithms=config("JWT_ALGO"))
    except:
        raise Exception("JWT token is invalid and cannot be decoded")
