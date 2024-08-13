from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("MYSQLHOST")
port = os.getenv("PORT")
name = os.getenv("MYSQLDATABASE")
user = os.getenv("MYSQLUSER")
password = os.getenv("MYSQLPASSWORD")

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

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
