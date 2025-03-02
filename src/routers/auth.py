from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from responseBody import Token
import os

import jwt
from jwt.exceptions import InvalidTokenError

ADMINPASS = os.environ.get('ADMIN_PSSWD') or os.urandom(16).hex()

KEY = os.environ.get('KEY') or os.urandom(32).hex()
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    tags=["Auth"]
)


async def access(token: Annotated[Token, Depends(oauth2_scheme)]):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found")
    payload = {"admin": False}
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        return None
    except Exception as e:
        print(e)
    finally:
        return payload.get("admin", False)


@router.post("/token", response_model=Token)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if data.password != ADMINPASS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    data = {"admin":True}
    token = jwt.encode(data, KEY, algorithm=ALGORITHM)
    return Token(access_token=token, token_type="bearer")

@router.get("/valitate")
async def validate_token(acc: Annotated[bool, Depends(access)]):
    return acc