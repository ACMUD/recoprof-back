from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from responseBody import Token
import os
import jwt
from dependencies.auth_dep import access
from utils.auth_logic import login_

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    tags=["Auth"]
)

ADMINPASS = os.environ.get('ADMIN_PSSWD') or os.urandom(16).hex()


@router.post("/token", response_model=Token)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if data.password != ADMINPASS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    token = await login_()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_INTERNAL_SERVER_ERROR, detail="Incorrect password")
    return token

@router.get("/valitate")
async def validate_token(acc: Annotated[bool, Depends(access)]):
    return acc
