import os
import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

load_dotenv()

host = os.getenv("MYSQLHOST")
port = os.getenv("PORT")
name = os.getenv("MYSQLDATABASE")
user = os.getenv("MYSQLUSER")
password = os.getenv("MYSQLPASSWORD")

DATABASE_URL = f"mysql://root:YWvvCMaQTLnIPFyMhCmXqpGWfhMDpFtP@viaduct.proxy.rlwy.net:11513/railway"

pymysql.install_as_MySQLdb()
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

metadata = MetaData()

# Crear el sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

con = engine.connect()
