from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.auth.jwt_hand import SECRET_KEY, ALGORITHM
from app.models.users.user import User
from sqlmodel import Session, select
from app.core.database import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return {"email": email, "name": user.name, "role": role, "department_id": user.id_department}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
