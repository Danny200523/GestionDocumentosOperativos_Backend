import enum
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlmodel import SQLModel, Field
class LoginAttempt(SQLModel, table=True):
    __tablename__ = "login_attempts"
    id: int = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    attempts: int = Field(default=0)
    is_blocked: bool = Field(default=False)
    last_attempt: datetime = Field(default_factory=datetime.utcnow)
