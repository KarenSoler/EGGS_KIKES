from sqlalchemy import Table, Column, Integer, String, Float, MetaData

metadata = MetaData()

egg_table = Table(
    'eggs',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('type_egg', String, nullable=False),
    Column('price', Float, nullable=False),
    Column('supplier', String, nullable=False)
)