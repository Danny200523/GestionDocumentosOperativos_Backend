import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.schemas import MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import SecretStr
from datetime import datetime, timedelta

load_dotenv()

# Configuración SMTP para testing con Mailtrap
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.mailtrap.io")
SMTP_PORT = int(os.getenv("SMTP_PORT", 2525))
SMTP_USER = os.getenv("SMTP_USER", "0f684e8cec65571261ab0db7092b6260")  # Usuario de Mailtrap
SMTP_PASS = os.getenv("SMTP_PASS", "tu_contraseña_mailtrap")  # Reemplaza con tu contraseña de Mailtrap

conf = ConnectionConfig(
    MAIL_USERNAME=SMTP_USER,
    MAIL_PASSWORD=SecretStr(SMTP_PASS),
    MAIL_FROM="itro.mapache@gmail.com",  # Email válido para el remitente
    MAIL_PORT=SMTP_PORT,
    MAIL_SERVER=SMTP_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_reset_email(to_email: str, token: str, base_url: str = "http://localhost:5173/restablecer-password"):
    subject = "Recuperación de contraseña"
    # Calcular fecha de expiración (15 minutos desde ahora)
    expiry = datetime.utcnow() + timedelta(minutes=15)
    reset_link = f"{base_url}/{token}"
    body = f"""
    Estimado/a usuario/a,

    Hemos recibido una solicitud para restablecer la contraseña de tu cuenta. Para continuar, haz clic en el siguiente enlace:

    {reset_link}

    Este enlace es válido por 15 minutos (hasta {expiry.strftime('%Y-%m-%d %H:%M:%S UTC')}). Si no solicitaste este cambio, por favor ignora este correo o contacta a nuestro equipo de soporte en itro.mapache@gmail.com.
    """

    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        from_email=SMTP_USER,
        body=body,
        subtype=MessageType.plain
    )

    try:
        print(f"[DEBUG] Intentando enviar correo a {to_email} usando {SMTP_HOST}:{SMTP_PORT}")
        fm = FastMail(conf)
        await fm.send_message(message)
        print(f"[DEBUG] Correo enviado exitosamente a {to_email}")
    except ConnectionErrors as e:
        print(f"[ERROR] Error de conexión al enviar correo: {e}")
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el correo: {e}")
