import stripe
import httpx
import os
from sqlmodel import Session
from app.db import engine
from app.schemas import OrderPay, RequestOrderPay

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY

MS_GAME_OPERATION_DEV_URL = os.getenv("MS_GAME_OPERATION_DEV_URL")

async def check_stock(game_id: int, quantity: int, token: str):
    
    try:
        headers = {"Authorization": token}
        async with httpx.AsyncClient() as client:
            url = f"{MS_GAME_OPERATION_DEV_URL}/{game_id}"
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                stock = data.get("resultado", {}).get("stock", 0)
                return stock >= quantity
            return False
    except Exception as e:
        print(e)
        return False
        
    

async def create_payment_session(session: Session, order_data: RequestOrderPay, folio: str, token: str):
    
    there_stock = await check_stock(order_data.game_id, order_data.unit, token)
    
    if not there_stock:
        return "Sin stock"
    
    unit_amount = int(order_data.price * 100)
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "mxn",
                    "product_data": {"name": order_data.name},
                    "unit_amount": unit_amount
                },
                "quantity": order_data.unit,
            }], 
            mode="payment",
            metadata={"folio": folio},
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
        )
        
        with Session(engine) as db_session:
    
            new_order = OrderPay(
                folio=folio,
                name=order_data.name,
                unit=order_data.unit,
                platforms_id=order_data.platforms_id,
                price=order_data.price,
                user_id=order_data.user_id,
                status="pendiente",
                game_id=order_data.game_id,
                stripe_session_id=session.id
            )
            
            db_session.add(new_order)
            db_session.commit()
            db_session.refresh(new_order)
            
        return session.url

    except Exception as e:
        print(f"Error en el servicio de pagos: {e}")
        return None