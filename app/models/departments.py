from sqlmodel import SQLModel, Field
from typing import Optional

class Department(SQLModel, table=True):
    __tablename__ = "departments"
    id_department: Optional[int] = Field(default=None, primary_key=True)
    name_department: str
