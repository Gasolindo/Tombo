from fastapi import HTTPException, Response, status
from fastapi import APIRouter
from config import DATABASE
import sqlite3


router = APIRouter(tags=["Tombo"])


@router.get("/")
async def view_material():
    with sqlite3.connect("tombo.db") as conn:
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        query = "SELECT * FROM tombos"
        cur.execute(query)

        return [dict(d) for d in cur.fetchall()]


@router.get("/tombo_user/{number}", status_code=200)
async def material_one(number: str):
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = f"SELECT tombos.tombo , materials.objeto , user.nome FROM tombos,materials,user WHERE tombo={number} AND tombos.id_materials = materials.id AND tombos.id_user = user.id"
            cursor = conn.execute(query)
            result = cursor.fetchone()
            print(result)
            if result == None:
                result = {
                    "mensagem": "Nenhum usuário tem esse tombo!",
                }
                return result
            return result
        except sqlite3:
            return "Erro"


@router.get("/tombo_exists/{number}", status_code=200)
async def material_one(number: str):
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = f"SELECT tombos.tombo , materials.objeto FROM tombos,materials WHERE tombo={number} AND tombos.id_materials = materials.id "
            cursor = conn.execute(query)
            result = cursor.fetchone()
            print(result)
            if result == None:
                result = {
                    "mensagem": "Tombo não encontrado",
                }
                return result
            return result
        except sqlite3:
            return "Erro"


@router.post("/", status_code=201)
async def post_tombo(request: dict, response: Response):
    body = request

    id_materials = body.get("id_materials")

    tombo = body.get("tombo")

    id_user = body.get("identificador")

    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row
            # cur = conn.cursor()
            if id_materials != None:
                query = f"SELECT COUNT (*) FROM materials WHERE id={id_materials} AND status_objeto <> 0 "

                cursor = conn.execute(query)
                result = cursor.fetchone()
                valor = list(result)

                if valor[0] == 0:
                    raise HTTPException(status_code=400, detail="Materials not found")

            if id_user != None:
                query = f"SELECT COUNT (*) FROM user WHERE cpf={id_user} AND status_ativo <> 0 "

                cursor = conn.execute(query)
                result = cursor.fetchone()
                valor = list(result)

                if valor[0] == 0:
                    raise HTTPException(status_code=400, detail="User not found")

            query = "INSERT INTO tombos (id_materials, tombo,id_user) VALUES (?, ?,?) RETURNING id"

            cursor = conn.execute(query, (id_materials, tombo, id_user))

            result = cursor.fetchone()

            conn.commit()

            body["id"] = result["id"]

            return body
        except sqlite3.InternalError as x:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error = str(x)
            if "tombo" in error and "UNIQUE" in error:
                return {"error:Already used numeracao"}


@router.get("/search")
async def view_material2():
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = "SELECT * FROM tombos INNER JOIN user ON tombos.id_user = user.id  "
            cursor = conn.execute(query)
            result = cursor.fetchall()

            conn.commit()

            return result

        except sqlite3.InternalError:
            # response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            # return response
            ...


@router.patch("/{tombo_id}", status_code=200)
async def new_matricula(body: dict, tombo_id: int):
    # print(tombo_id)
    tombo = body.get("tombo")
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = f"UPDATE tombos SET tombo = {tombo}  WHERE id = {tombo_id}"

            conn.execute(query)
            conn.commit()

        except sqlite3.InternalError:
            print("ok")
            ...
        return body


@router.delete("/{id}", status_code=204)
async def deletar_user(id: int):
    # print(matricula_user)
    # matricula = body.get("matricula")
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row
            query = f"DELETE FROM tombos WHERE id = {id}"
            conn.execute(query)
            conn.commit()

        except sqlite3.InternalError:
            return {"user": [f"delete user {id}"]}
