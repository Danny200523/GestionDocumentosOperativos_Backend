from sqlmodel import SQLModel, Field
from typing import Optional

class ResetPasswordToken(SQLModel, table=True):
    __tablename__ = "reset_password_tokens"
    id_token: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    token: str
