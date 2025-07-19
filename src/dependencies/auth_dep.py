from fastapi import HTTPException, status, Depends
from typing import Annotated
from responseBody import Token
from fastapi.security import OAuth2PasswordBearer
from utils.auth_logic import validate_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def access(token: Annotated[Token, Depends(oauth2_scheme)]):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    access_value = await validate_token(token)
    if not access_value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return access_value
