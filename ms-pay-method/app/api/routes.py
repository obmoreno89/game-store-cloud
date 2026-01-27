from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from sqlmodel import Session
from fastapi.security import HTTPBearer
from app.utils import generat_uuid
from app.schemas import OrderPayResponse, RequestOrderPay
from app.db import get_session
from app.services import get_current_user, create_payment_session, process_stripe_event

auth_scheme = HTTPBearer()
router = APIRouter(tags=["Metodo Pago"])

@router.post("/game-store/v1/metodos/orden", response_model=OrderPayResponse, dependencies=[Depends(auth_scheme)])
async def order(request: Request, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user), order_data: RequestOrderPay = Body()):
    token = request.headers.get("Authorization")
    folio = generat_uuid()
    new_order = await create_payment_session(session, order_data, folio, token)
    
    if not new_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "folio": folio,
                "mensaje": "No se pudo crear la orden de pago"
            }
        )
        
    if new_order == "Sin stock":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "folio": folio,
            "mensaje": "No hay unidades disponibles"
        })
         
    
    return OrderPayResponse(
      folio=folio,
      mensaje="Operación exitosa",
      resultado={"url": new_order}
    )


@router.post("/game-store/v1/metodos/webhooks/stripe")
async def stripe_weebhook(request: Request, session: Session = Depends(get_session)):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    
    if not sig_header:
        raise HTTPException(status_code=400, detail="Falta firma de Stripe")
    
    success = await process_stripe_event(payload, sig_header, session)
    
    if success:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=400, detail="Error en webhook")
    
    
