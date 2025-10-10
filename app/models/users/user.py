from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    id_user: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    # hacer que el password pueda recibir un hash de password
    password: str 
    role: str = "operator"
    id_department: int

class UserCreate(SQLModel):
    name: str
    email: str
    password: str
    role: str = "operator"
    id_department: int 

class UserRead(SQLModel):
    name: str
    email: str
    role: str

