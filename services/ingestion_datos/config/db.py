import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USERNAME = os.getenv("DB_USERNAME", default="root")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="adminadmin")
# DB_HOSTNAME = os.getenv("DB_HOSTNAME", default="35.223.246.149")
DB_HOSTNAME = os.getenv("DB_HOSTNAME", default="localhost")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/saludtech"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()