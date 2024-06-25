from fastapi import APIRouter, HTTPException
import sqlite3
from tombo.helpers.myhash import verify_hash
from config import DATABASE
from tombo.helpers.token import create_token_jwt
from pydantic import BaseModel


router = APIRouter(tags=["Login"])


class Login(BaseModel):
    email: str
    password: str


@router.post("/", status_code=200)
async def login_user(body: dict, login: Login):
    required_fields = ["email", "password"]

    fields_not_provided = []

    for k in required_fields:
        if k not in body.keys():
            fields_not_provided.append(k)

    if len(fields_not_provided):
        return {"required": ", ".join(required_fields)}

    email, password = body.get("email"), body.get("password")

    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = (
                f"SELECT `password`, `id`, `nivel` FROM user WHERE email = '{email}'"
            )

            cursor = conn.execute(query)
            result = cursor.fetchone()

            if not verify_hash(password, result["password"]):
                return "incorect email or password"

            print({"verify": verify_hash(password, result["password"])})

            encoded_token = create_token_jwt(
                result["id"],
                result["nivel"],
            )

            return login, {
                "access_token": encoded_token,
                "token_type": "bearer",
            }

        except sqlite3.InternalError:
            if not email or None:
                raise HTTPException(
                    status_code=403, detail="Email ou password incorrect!"
                )


# @router.get("/", status_code=200)
# async def token(encoded_jwt, id):
#     if encoded_jwt == True:
#         return "Token validated!"
