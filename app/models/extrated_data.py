from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, JSON

class ExtractedData(SQLModel, table=True):
    __tablename__ = "extrated_data"  
    id_table: Optional[int] = Field(default=None, primary_key=True)
    department_id: int
    table_data: dict = Field(sa_column=Column(JSON, nullable=False))
    file_name: str = Field(default="Sin nombre", max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="Aprobado", max_length=50)
