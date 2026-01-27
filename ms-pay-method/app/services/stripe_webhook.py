import stripe
import httpx
from sqlmodel import Session, select
from app.schemas import OrderPay
from datetime import datetime
import os

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
MS_GAMES_OPERATION_PATCH_URL_DEV = os.getenv("MS_GAMES_OPERATION_PATCH_URL_DEV")
SECRET_KEY_INTERNAL = os.getenv("SECRET_KEY_INTERNAL")

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
        
        folio = session_data.get("metadata", {}).get("folio")
        
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
                
    return True


async def notify_inventory_update(game_id: int, quantity: int):
    
    url = f"{MS_GAMES_OPERATION_PATCH_URL_DEV}/{game_id}"
    content_headers = {
        "x-internal-secret": SECRET_KEY_INTERNAL,
        "Content-Type": "aplication/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json={"stock": quantity}, headers=content_headers)
            if response.status_code == 200:
                print("Operación exitosa")
            else:
                print("Error en la actualización")
    except Exception as e:
        print(e)
    