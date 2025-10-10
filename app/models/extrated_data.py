from sqlmodel import SQLModel, Field
from typing import Optional

class ExtratedData(SQLModel, table=True):
    __tablename__ = "extrated_data"
    id_table: Optional[int] = Field(default=None, primary_key=True)
    department_id: int
    table_data: str  # JSON as string
