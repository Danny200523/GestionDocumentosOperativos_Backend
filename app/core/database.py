from sqlmodel import SQLModel, create_engine, Session
import os

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "docsflow")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

# Import all models to ensure they are registered
from app.models import User, Department, ExtratedData, KeyData, ResetPasswordToken, LoginAttempt

# Create tables
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
