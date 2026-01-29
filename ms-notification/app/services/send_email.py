import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from sqlmodel import Session, select
from app.db import engine
from app.schemas import Notification
from app.template import html_pay_confirmation

conf = ConnectionConfig(
    MAIL_USERNAME= os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD= os.getenv("MAIL_PASSWORD"),
    MAIL_FROM= os.getenv("MAIL_USERNAME"),
    MAIL_PORT= os.getenv("MAIL_PORT"),
    MAIL_SERVER= os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS= os.getenv("MAIL_STARTTLS"),
    MAIL_SSL_TLS= os.getenv("MAIL_SSL_TLS"),
    USE_CREDENTIALS= os.getenv("USE_CREDENTIALS"),
    VALIDATE_CERTS= os.getenv("VALIDATE_CERTS")   
)

async def email_send(email_to: str, folio: str, game_name):
    is_same_folio = False
    
    
    with Session(engine) as session:
        print(f"Verificando existencia del folio {folio}")
        
        statement = select(Notification).where(Notification.folio == folio)
        existing_folio = session.exec(statement).first()
        
        if existing_folio: 
           is_same_folio = True
           return is_same_folio
        
        print(f"Procesando correo para {email_to} - folio {folio}")
        
        log = Notification(
           folio=folio,
           email=email_to,
           status="pendiente"
        )
        
        session.add(log)
        session.commit()
        session.refresh(log)
        
        html_body = html_pay_confirmation(game_name, folio)
        
        message = MessageSchema(
            subject=f"Compra exitosa - {folio}",
            recipients=[email_to],
            body=html_body,
            subtype=MessageType.html 
        )
        
        fm = FastMail(conf)
        
        try:
            await fm.send_message(message)
            log.status = "enviado"
            is_same_folio = False
            print(f"Correo enviado a {email_to}")
        
        except Exception as e:
            log.status = "fallido"
            print(f"Error enviando correo - {e}")
            
        finally:
           if log:
                session.add(log)
                session.commit()
                session.refresh(log)
        
        return is_same_folio
        
        
       
        
        