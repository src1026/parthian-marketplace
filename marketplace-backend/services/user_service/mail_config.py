from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from dotenv import load_dotenv

load_dotenv()

class EmailSchema(BaseModel):
    email: EmailStr

def str_to_bool(value):
    return value.lower() in ["true", "1", "t", "yes"]

MAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=str_to_bool(os.getenv("MAIL_STARTTLS", "True")),
    MAIL_SSL_TLS=str_to_bool(os.getenv("MAIL_SSL_TLS", "False")),
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_verification_email(email: str, token: str):
    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=f"""
        <p>Click the link to verify your email:</p>
        <a href="http://localhost:8001/user/auth/verify?token={token}">Verify Email</a>
        """,
        subtype="html"
    )
    fm = FastMail(MAIL_CONFIG)
    await fm.send_message(message)
