import stripe
import httpx
from sqlmodel import Session, select
from app.schemas import OrderPay, EmailRequest
from datetime import datetime
from app.utils import content
import os

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
MS_GAMES_OPERATION_PATCH_URL_DEV = os.getenv("MS_GAMES_OPERATION_PATCH_URL_DEV")
MS_NOTIFICATION_DEV_URL= os.getenv("MS_NOTIFICATION_DEV_URL")

async def process_stripe_event(payload: bytes, sig_header: str, session: Session):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print(f"Firma invalida {e}")
        return False
    
    if event["type"] == "checkout.session.completed":
        session_data = event["data"]["object"]
        
        metadata = session_data.get("metadata", {})
        
        folio = metadata.get("folio")
       
        email = metadata.get("email_usuario") or session_data.get("customer_details", {}).get("email")
        
        if folio:
            statement = select(OrderPay).where(OrderPay.folio == folio)
            order = session.exec(statement).first()
            
            
            if order and order.status == "pendiente":
                order.status = "pagado"
                order.date_order_pay = datetime.now()
                session.add(order)
                session.commit()
                print(f"Orden {folio} pagada")
                
                await notify_inventory_update(order.game_id, order.unit)
                
                game_name = order.name
                
                if email and game_name:
                    email_data = EmailRequest(
                        email=email,
                        folio=folio,
                        game_name=game_name
                    )
                    
                    await send_notification(email_data)
                else: 
                    print("Faltan datos por enviar")
                
    return True


async def notify_inventory_update(game_id: int, quantity: int):
    
    url = f"{MS_GAMES_OPERATION_PATCH_URL_DEV}/{game_id}"
    
    content_headers = content()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json={"stock": quantity}, headers=content_headers)
            if response.status_code == 200:
                print("Operación exitosa")
            else:
                print("Error en la actualización")
    except Exception as e:
        print(e)
        

async def send_notification(email_data: EmailRequest):
    url_ms_notification = f"{MS_NOTIFICATION_DEV_URL}"
    
    content_headers = content()
    
    payload = {
        "folio": email_data.folio,
        "email": email_data.email,
        "game_name": email_data.game_name
    }
    
    try: 
        async with httpx.AsyncClient() as client:
            response = await client.post(url_ms_notification, json=payload, headers=content_headers)
            if response.status_code == 200:
                print("Operación exitosa")
            else:
                print("Error al enviar el correo")
    except Exception as e:
        print(e)
        
    
   
    
    