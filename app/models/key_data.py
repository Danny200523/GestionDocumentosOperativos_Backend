from sqlmodel import SQLModel, Field
from typing import Optional

class KeyData(SQLModel, table=True):
    __tablename__ = "key_data"
    id_data: Optional[int] = Field(default=None, primary_key=True)
    department_id: int
    table_id: int
    key: str
    value: str
