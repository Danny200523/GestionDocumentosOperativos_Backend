from sqlmodel import SQLModel, create_engine, Session
import os
from sqlalchemy import text

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "docsflow")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)

SQLModel.metadata.create_all(engine)

with engine.begin() as conn:
    cols = conn.execute(text(
        """
        SELECT COLUMN_NAME FROM information_schema.columns
        WHERE table_schema = DATABASE() AND table_name = 'extrated_data'
        """
    )).fetchall()
    existing = {c[0] for c in cols}
    if 'file_name' not in existing:
        conn.execute(text("ALTER TABLE extrated_data ADD COLUMN file_name VARCHAR(255) NULL DEFAULT 'Sin nombre'"))
    if 'created_at' not in existing:
        conn.execute(text("ALTER TABLE extrated_data ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"))
    if 'status' not in existing:
        conn.execute(text("ALTER TABLE extrated_data ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'Aprobado'"))


def get_session():
    with Session(engine) as session:
        yield session
