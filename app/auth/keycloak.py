import jwt
import requests

from app.config.config import (
    JWKS_URL,
    ISSUER
)


jwks_client = jwt.PyJWKClient(JWKS_URL)


def verify_token(token: str):
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=ISSUER,
            options={"verify_aud": False}
        )

        print("PAYLOAD:", payload)

        return payload

    except Exception as e:
        print("JWT ERROR:", repr(e))
        raise