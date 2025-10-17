# utils/db_connection.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Example DB URL: postgresql+psycopg2://user:pass@localhost:5432/cricdb
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cricbuzz.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    return SessionLocal()
