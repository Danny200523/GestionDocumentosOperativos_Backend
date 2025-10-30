from sqlmodel import SQLModel, create_engine, Session
import os
from sqlalchemy import text


DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL and DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://")

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
    if 'user_id' not in existing:
        conn.execute(text("ALTER TABLE extrated_data ADD COLUMN user_id INT NULL"))

# Sesión de base de datos
def get_session():
    with Session(engine) as session:
        yield session


