from typing import List
from sqlalchemy import insert, select
from fastapi import APIRouter, HTTPException, Response, status, Depends
from starlette.status import HTTP_204_NO_CONTENT
from models.egg_model import egg_table
from schemas.egg_schema import Egg, EggCreate, EggUpdate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config.db import get_db

eggs_router = APIRouter()


@eggs_router.get("/eggs", response_model=List[Egg])
def get_eggs(db: Session = Depends(get_db)):
    keys = [
        "id",
        "type_egg",
        "price",
        "supplier"
    ]
    query = select(egg_table)
    results = db.execute(query).fetchall()

    data = [dict(zip(keys, results)) for results in results]
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
        db.commit()
        inserted_id = result.inserted_primary_key[0]
        print("print2")

        query = select(egg_table).where(egg_table.c.id == inserted_id)
        print("print3")
        record = db.execute(query).fetchone()
        print("print4")

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
def view_egg(id: int, db: Session = Depends(get_db)):
    # Consulta para seleccionar el huevo por su id
    query = select(egg_table).where(egg_table.c.id == id)
    result = db.execute(query).fetchone()  # Obtiene el primer resultado

    if result:
        # Mapeo de columnas a claves para formar un diccionario
        keys = ["id", "type_egg", "price", "supplier"]
        data = dict(zip(keys, result))
        return data
    else:
        raise HTTPException(status_code=404, detail="Egg not found")


@eggs_router.delete("/eggs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_egg(id: int, db: Session = Depends(get_db)):
    try:
        print("Attempting to delete egg with id:", id)

        # Ejecuta la eliminación
        result = db.execute(egg_table.delete().where(egg_table.c.id == id))

        # Verifica si realmente se eliminó algo
        if result.rowcount == 0:
            db.rollback()  # Revertir la transacción si no se eliminó nada
            raise HTTPException(status_code=404, detail="Egg not found")

        print("Committing transaction")
        db.commit()  # Confirmar los cambios en la base de datos
        print("Transaction committed")

        return Response(status_code=HTTP_204_NO_CONTENT)

    except SQLAlchemyError as e:
        print("Error occurred:", e)
        db.rollback()  # Revertir la transacción en caso de error
        raise HTTPException(status_code=500, detail="Database error: " + str(e))


@eggs_router.put("/eggs/{id}", response_model=Egg)
def update_egg(id: int, egg: EggUpdate, db: Session = Depends(get_db)):
    try:
        # Crear la sentencia de actualización
        update_stmt = (
            egg_table.update()
            .where(egg_table.c.id == id)
            .values(
                type_egg=egg.type_egg,
                price=egg.price,
                supplier=egg.supplier
            )
        )

        # Ejecutar la actualización
        result = db.execute(update_stmt)

        # Verificar si realmente se actualizó algo
        if result.rowcount == 0:
            db.rollback()  # Revertir la transacción si no se actualizó nada
            raise HTTPException(status_code=404, detail="Egg not found")

        # Confirmar la transacción
        db.commit()

        # Consultar el registro actualizado
        query = select(egg_table).where(egg_table.c.id == id)
        record = db.execute(query).fetchone()

        if record:
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
