from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ExtratedData(SQLModel, table=True):
    __tablename__ = "extrateddata"  # 👈 asegúrate que el nombre coincide con tu tabla real
    id_table: Optional[int] = Field(default=None, primary_key=True)
    department_id: int
    table_data: str  # JSON guardado como string
    file_name: str = Field(default="Sin nombre", max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="Aprobado", max_length=50)