from typing import List
from sqlalchemy import insert, select
from fastapi import APIRouter, HTTPException, Response, status, Depends
from starlette.status import HTTP_204_NO_CONTENT
from config.db import con
from models.egg_model import egg_table
from schemas.egg_schema import Egg, EggCreate, EggUpdate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config.db import get_db

eggs_router = APIRouter()


@eggs_router.get("/eggs", response_model=List[Egg])
def get_eggs():
    keys = [
        "id",
        "type_egg",
        "price",
        "supplier"
    ]
    query = select(egg_table)
    results = con.execute(query).first()

    data = [dict(zip(keys, results)) for result in results]
    return data


@eggs_router.post("/eggs", response_model=Egg)
def create_egg(egg: EggCreate, db: Session = Depends(get_db)):
    print("create_egg")
    print(egg)
    new_egg = {
        "type_egg": egg.type_egg,
        "price": egg.price,
        "supplier": egg.supplier
    }
    print(new_egg)
    try:
            result = db.execute(insert(egg_table).values(new_egg))
            print("Print1")
            inserted_id = result.inserted_primary_key[0]
            print("print2")

            query = select(egg_table).where(egg_table.c.id == inserted_id)
            print("print3")
            record = db.execute(query).fetchone()
            print("print4")

            db.commit()

            if record:
                print(record)
                print(type(record))
                keys = [
                    "id",
                    "type_egg",
                    "price",
                    "supplier",
                ]
                data = dict(zip(keys, record))
                return data

            else:
                raise HTTPException(status_code=404, detail="Egg not found")
    except Exception as e:
        db.rollback()  # Hacer rollback si algo falla
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@eggs_router.get("/eggs/{id}", response_model=Egg)
def view_egg(id: int):
    query = select(egg_table).where(egg_table.c.id == id)
    record = con.execute(query).first()
    if record:
        return dict(record)
    else:
        raise HTTPException(status_code=404, detail="Egg not found")


@eggs_router.delete("/eggs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_egg(id: int):
    result = con.execute(egg_table.delete().where(egg_table.c.id == id))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Egg not found")
    return Response(status_code=HTTP_204_NO_CONTENT)


@eggs_router.put("/eggs/{id}", response_model=Egg)
def update_egg(id: int, egg: EggUpdate):
    update_stmt = egg_table.update().where(egg_table.c.id == id).values(
        type_egg=egg.type_egg,
        price=egg.price,
        supplier=egg.supplier
    )
    result = con.execute(update_stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Egg not found")

    query = select(egg_table).where(egg_table.c.id == id)
    record = con.execute(query).fetchone()
    if record:
        return dict(record)
    else:
        raise HTTPException(status_code=404, detail="Egg not found")
