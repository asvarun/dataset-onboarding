from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import database

app = FastAPI()

conn, cursor = database()


class Table(BaseModel):
    id: Optional[int]
    table_name: str
    table_key: str
    delete_key: str
    partitioned_by: str
    delta_table: bool
    dependency_dag: Optional[str]
    created_at: Optional[datetime]


@app.get("/")
async def root():
    return {"message": "NIKE Table Onboarding"}


@app.get("/tables")
async def get_tables():
    cursor.execute(""" SELECT * FROM table_onboarding ORDER BY id DESC """)
    posts = cursor.fetchall()
    return posts


@app.post("/tables", status_code=status.HTTP_201_CREATED)
async def post_table(table: Table):
    cursor.execute(
        """INSERT INTO table_onboarding (table_name, table_key, delete_key, partitioned_by, delta_table, 
        dependency_dag) VALUES (%s, %s, %s, %s, %s, %s) RETURNING * """,
        (table.table_name, table.table_key, table.delete_key, table.partitioned_by, table.delta_table,
         table.dependency_dag))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/tables/{id}", status_code=status.HTTP_200_OK)
async def get_table(id: int):
    cursor.execute(""" SELECT * FROM table_onboarding WHERE id = %s """, (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return post


@app.delete("/tables/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(id: int):
    cursor.execute(""" DELETE FROM table_onboarding WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/tables/{id}")
async def update_table(id: int, table: Table):
    cursor.execute(
        """UPDATE table_onboarding SET table_name = %s, table_key = %s, delete_key = %s, partitioned_by = %s, 
        delta_table = %s, dependency_dag = %s WHERE id = %s RETURNING * """,
        (table.table_name, table.table_key, table.delete_key, table.partitioned_by, table.delta_table,
         table.dependency_dag, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    return {"data": updated_post}
