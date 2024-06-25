from fastapi import Response, status
from fastapi import APIRouter
import sqlite3
from config import DATABASE
from pydantic import BaseModel


router = APIRouter(tags=["Materials"])


@router.get("/", status_code=200)
async def all_materials():
    with sqlite3.connect("tombo.db") as conn:
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        query = "SELECT * FROM materials"
        cur.execute(query)
        return [dict(d) for d in cur.fetchall()]


class Item(BaseModel):
    objeto: str


@router.post("/", status_code=200)
async def insert_material(item: Item, objeto: dict, response: Response):

    # print(request)
    # body = request

    required_fields = ["objeto"]

    fields_not_provided = []

    for k in required_fields:
        if k not in objeto.keys():
            fields_not_provided.append(k)

    if len(fields_not_provided):
        return {"required": ", ".join(required_fields)}

    objeto = objeto.get("objeto")
    print(objeto)
    # status_objeto = body.get("status_objeto")

    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            query = "INSERT INTO materials(objeto) VALUES (?)"
            cursor = conn.execute(query, [objeto])

            result = cursor.fetchall()

            conn.commit()

            return item, [dict(d) for d in cur.fetchall()]

        except sqlite3.IntegrityError:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


@router.patch("/{objeto_id}", status_code=200)
async def desactive_materials(objeto_id: int):
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = f"UPDATE materials SET status_objeto = 0 WHERE id = {objeto_id} "
            # query2 = f"UPDATE tombos SET id_user = NULL WHERE id_user={user_id} "

            print(query)
            conn.execute(query)

            # conn.execute(query2)

            # result = cursor.fetchone()

            conn.commit()

            # print(result)

        except sqlite3.InternalError:
            ...


@router.patch("/activate/{objeto_id}", status_code=200)
async def activate_materials(objeto_id: int):
    with sqlite3.connect(DATABASE) as conn:
        try:
            conn.row_factory = sqlite3.Row

            query = f"UPDATE materials SET status_objeto = 1  WHERE id = {objeto_id} "

            print(query)
            conn.execute(query)

            conn.commit()

        except sqlite3.InternalError:
            ...
