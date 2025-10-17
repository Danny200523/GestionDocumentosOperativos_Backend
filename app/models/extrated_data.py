from sqlmodel import SQLModel, Field, Column, Integer, JSON, TIMESTAMP, func, ForeignKey
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, JSON

class ExtractedData(SQLModel, table=True):
    __tablename__ = "extrated_data"  
    id_table: Optional[int] = Field(default=None, primary_key=True)
    department_id: int
    user_id: Optional[int] = Field(default=None, foreign_key="users.id_user")
    table_data: dict = Field(sa_column=Column(JSON, nullable=False))
    file_name: str = Field(default="Sin nombre", max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="Aprobado", max_length=50)



class ExtractedDataUser(SQLModel, table=True):
    id_table: Optional[int] = Field(default=None, primary_key=True)
    department_id: int = Field(foreign_key="departments.id_department")
    user_id: int = Field(foreign_key="users.id_user")  
    file_name: str
    table_data: dict = Field(sa_column=Column(JSON))
    status: str = Field(default="Pendiente")
    created_at: datetime = Field(default_factory=datetime.utcnow)
