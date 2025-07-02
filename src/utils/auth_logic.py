from responseBody import Token
from jwt.exceptions import InvalidTokenError
import os
import jwt

KEY = os.environ.get('KEY') or os.urandom(32).hex()
ALGORITHM = "HS256"

async def login_():
    data = {"admin":True}
    token = jwt.encode(data, KEY, algorithm=ALGORITHM)
    return Token(access_token=token, token_type="bearer")

async def validate_token(token: str):
    payload = {"admin": False}
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
    except InvalidTokenError:
        return None
    except Exception as e:
        print(e)
    finally:
        return payload.get("admin", False)