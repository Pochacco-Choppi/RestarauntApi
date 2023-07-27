import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

db_user = os.environ["DATABASE_USER"]
db_password = os.environ["DATABASE_PASSWORD"]
db_host = os.environ["DATABASE_HOST"]
db_port = os.environ["DATABASE_PORT"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

my_metadata = MetaData()
    
class Base(DeclarativeBase):
    metadata = my_metadata
