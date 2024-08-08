from pydantic import BaseModel
from typing import Optional


class EggCreate(BaseModel):
    type_egg: str
    price: float
    supplier: str


class EggUpdate(BaseModel):
    type_egg: Optional[str] = None
    price: Optional[float] = None
    supplier: Optional[str] = None


class Egg(EggCreate):
    id: int
