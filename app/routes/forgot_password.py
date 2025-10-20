import os
from dotenv import load_dotenv
from app.utils.email import send_reset_email

from fastapi import APIRouter, Depends, HTTPException, Form, Query
from pydantic import EmailStr
from sqlmodel import Session, select
from app.models import User
from app.models.forgot_password import ForgotPasswordRequest, ResetPasswordToken
from app.core.database import get_session
from app.auth.validar_password import hash_password
from datetime import datetime

load_dotenv()
# URL base para el enlace de restablecimiento (endpoint para resetear)
BASE_URL = "http://localhost:5173/restablecer-password"

router = APIRouter()

@router.post("/forgot-password")
async def forgot_password(email: EmailStr = Query(...), session: Session = Depends(get_session)):
    # Modelo Pydantic incluido para validar el correo (ForgotPasswordRequest)

    # Buscar usuario por email
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    # Respuesta genérica para evitar enumeración de usuarios
    generic_response = {
        "message": "Si el correo está registrado, recibirás un enlace para restablecer la contraseña."
    }

    if not user:
        print(f"[DEBUG] Usuario no encontrado para email: {email}")
        return generic_response

    print(f"[DEBUG] Usuario encontrado: {user.email}, generando token")
    # Generar token único con expiración
    if user.id_user is None:
        print(f"[DEBUG] Usuario sin ID válido: {user.email}")
        return generic_response
    token_obj = ResetPasswordToken.generate_token(user_id=user.id_user)
    session.add(token_obj)
    session.commit()
    session.refresh(token_obj)

    # Enviar correo con token
    try:
        await send_reset_email(user.email, token_obj.token, BASE_URL)
    except HTTPException:
        # Manejar error de envío
        raise HTTPException(status_code=500, detail="Error al enviar el correo de recuperación.")

    return generic_response


@router.post("/auth/reset-password")
def reset_password(
    token: str = Form(...),
    new_password: str = Form(...),
    session: Session = Depends(get_session)
):
    # Buscar token en la base de datos
    statement = select(ResetPasswordToken).where(ResetPasswordToken.token == token)
    token_obj = session.exec(statement).first()

    # Verificar si el token existe
    if not token_obj:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")

    # Buscar usuario asociado al token
    user_statement = select(User).where(User.id_user == token_obj.user_id)
    user = session.exec(user_statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Encriptar y actualizar la nueva contraseña
    user.password = hash_password(new_password)
    session.add(user)

    # Eliminar token de la tabla para que no se reutilice
    session.delete(token_obj)

    # Confirmar los cambios
    session.commit()
    session.refresh(user)

    return {"msg": "Contraseña actualizada correctamente"}

