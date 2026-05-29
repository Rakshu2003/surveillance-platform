from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pymongo import MongoClient
import redis
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client["surveillance"]

redis_client = redis.from_url(os.getenv("REDIS_URL"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()