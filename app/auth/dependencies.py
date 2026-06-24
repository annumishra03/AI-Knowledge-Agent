from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

from app.auth.keycloak import verify_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials

        payload = verify_token(token)

        print("USER:", payload["preferred_username"])

        return payload

    except Exception as e:

        print("AUTH ERROR:", repr(e))

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )