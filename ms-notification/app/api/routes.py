import os
from fastapi import APIRouter, Depends, Body, HTTPException, status, BackgroundTasks, Header
from sqlmodel import Session
from app.db import get_session
from app.schemas import EmailResponse, EmailRequest
from app.services import email_send
from app.utils import generat_uuid

router = APIRouter(tags=["Notificaciones"])

SECRET_KEY_INTERNAL = os.getenv("SECRET_KEY_INTERNAL")

@router.post("/game-store/v1/notificaciones", response_model=EmailResponse)
async def email(background_task: BackgroundTasks,session: Session = Depends(get_session), email_data: EmailRequest = Body(), x_internal_secret: str = Header(None)):
    folio_error_or_success = generat_uuid()
    
    if x_internal_secret != SECRET_KEY_INTERNAL:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"folio": folio_error_or_success, "mensaje": "No estas autorizado"})
    
    is_same_folio = await email_send(email_data.email, email_data.folio, email_data.game_name)
    
    
    if is_same_folio:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail={
                "folio": folio_error_or_success,
                "mensaje": "El folio ya existe"
            }
        )
        
    
    background_task.add_task(
        email_send,
        email_to=email_data.email,
        folio=email_data.folio,
        game_name=email_data.game_name
    )
    
    return EmailResponse(
        folio=folio_error_or_success,
        mensaje="Operación exitosa"
    )
        
    
    