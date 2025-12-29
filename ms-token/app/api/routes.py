from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.services.security import create_access_token
from app.schemas.models import Token
from app.utils import uuid
from app.api.doc.token import UNAUTHORIZED_RESPONSE

router = APIRouter(tags=["Autenticación"])

MOCK_USERNAME = "admin"
MOCK_PASSWORD = "password123"



@router.post("/oauth2/v1/token", response_model=Token, responses=UNAUTHORIZED_RESPONSE)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    folio = uuid.uuid_generate()
    if form_data.username == MOCK_USERNAME and form_data.password == MOCK_PASSWORD:
        user_data = {"username": MOCK_USERNAME}
    else: 
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder({ "folio": folio,"mensaje": "Credenciales incorrectas"}),
        )

                   
    access_token = create_access_token(
        data={"username": user_data["username"]}
    )
    
    return {"folio": folio, "mensaje": "Operación exitosa", "resultado": {"access_token": access_token, "token_type": "bearer"}}    
    
        