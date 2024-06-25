from datetime import datetime, timedelta
import sqlite3
from fastapi import HTTPException, Request
from passlib.context import CryptContext
from jose import JWTError, jwt

from config import DATABASE


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "273a0418d8f4b11497112c3c9e77bfc2b8f40c93ad91a1c25a54cea6e6ce33c3"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 20


def create_token_jwt(id, nivel):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(id), "nivel": (nivel)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(encoded_jwt):
    try:
        decode_jwt = jwt.decode(
            encoded_jwt,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")


# async def verify_token2(request: Request):
#     token = request.headers["Authorization"]

#     if not token:
#         raise HTTPException(status_code=401, detail="Unauthorized")


async def verify_api_key(request: Request):
    api_key = request.headers.get("X-Api-Key")
    request.auth
    if api_key != f"{SECRET_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")


async def nivel():
    with sqlite3.connect(DATABASE) as conn:

        cur = conn.cursor()
        query = "SELECT nivel FROM user "
        cur.execute(query)

        if not nivel == "admin":
            raise HTTPException(status_code=403, detail="user not authorized")
