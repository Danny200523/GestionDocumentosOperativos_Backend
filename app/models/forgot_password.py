from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timedelta
import uuid
from pydantic import BaseModel, EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(SQLModel):
    token: str
    new_password: str


class ResetPasswordToken(SQLModel, table=True):
    __tablename__ = "reset_password_tokens"

    id_token: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    token: str

    @classmethod
    def generate_token(cls, user_id: int):
        # Generar token único usando uuid
        token = uuid.uuid4().hex
        return cls(user_id=user_id, token=token)
