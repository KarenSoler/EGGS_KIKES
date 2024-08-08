from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/kikes_eggs"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.bind = engine

# Crear el sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


con = engine.connect()
