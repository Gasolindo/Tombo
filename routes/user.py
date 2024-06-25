from fastapi import APIRouter
from fastapi import Response, status, HTTPException, Body
from tombo.helpers.myhash import generate_hash
from config import DATABASE
from pydantic import BaseModel


import sqlite3


router = APIRouter(tags=["User"])


@router.get("/")
async def view():
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.cursor()
            query = "SELECT * FROM user"
            cur.execute(query)
        except HTTPException:
            return HTTPException

        return [dict(d) for d in cur.fetchall()]


class User(BaseModel):
    nome: str
    matricula: int
    cpf: int
    celular: int
    email: str
    password: str


@router.post("/", status_code=201)
async def post_data(user: User, request: dict = Body(), response: Response = None):

    required_fields = ["nome", "matricula", "cpf", "celular", "email", "password"]

    fields_not_provided = []

    for k in required_fields:
        if k not in request.keys():
            fields_not_provided.append(k)

    if len(fields_not_provided):
        return {"required": ", ".join(required_fields)}

    nome, matricula, cpf, celular, email, password = (
        request.get("nome"),
        request.get("matricula"),
        request.get("cpf"),
        request.get("celular"),
        request.get("email"),
        request.get("password"),
    )

    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row
            password = generate_hash(password)
            print(password)

            query = "INSERT INTO user (nome, matricula,cpf,celular,email,password) VALUES (?, ?, ?, ?, ?, ?) RETURNING id"
            cursor = conn.execute(
                query, [nome, matricula, cpf, celular, email, password]
            )

            result = cursor.fetchone()

            conn.commit()

            request["id"] = result["id"]

            return request, user

        except sqlite3.IntegrityError as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            str_error = str(e)

            if "matricula" in str_error and "UNIQUE" in str_error:
                return {"error": "Matrícula existente"}

            elif "email" in str_error and "UNIQUE" in str_error:
                return {"error": "E-mail já cadastrado"}

            elif "cpf" in str_error and "UNIQUE" in str_error:
                return {"error": "CPF já cadastrado"}


@router.get("/user_material/{user}", status_code=200)
async def view_user(user: int):
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = f"SELECT * FROM user INNER JOIN tombos ON user.id = tombos.id_user WHERE tombo={user} "

            cursor = conn.execute(query)
            result = cursor.fetchall()

            conn.commit()

            if result == []:
                return "User not exist!"

            return result

        except sqlite3.InternalError:
            return "erro 500!"
            # response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            # return response
            # ...


@router.patch("/matricula_update/{user_id}", status_code=200)
async def new_matricula(body: dict, user_id: int):
    print(user_id)
    matricula = body.get("matricula")

    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = f"UPDATE user SET matricula = {matricula}  WHERE id = {user_id} "
            conn.execute(query)

            conn.commit()

            return body

        except sqlite3.InternalError:

            return body
        ...


@router.patch("desativado/{user_id}", status_code=200)
async def desactive_user(user_id: int):
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = f"UPDATE user SET status_ativo = 0 WHERE id = {user_id} "
            query2 = f"UPDATE tombos SET id_user = NULL WHERE id_user={user_id} "

            print(query)
            conn.execute(query)

            conn.execute(query2)

            # result = cursor.fetchone()

            conn.commit()

        except sqlite3.InternalError:
            ...


@router.patch("activate/{user_id}", status_code=200)
async def activate_materials(user_id: int):
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = f"UPDATE user SET status_ativo = 1  WHERE id = {user_id} "

            print(query)
            conn.execute(query)

            conn.commit()

        except sqlite3.InternalError:
            ...
