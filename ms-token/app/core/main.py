from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.utils import uuid



app = FastAPI(
    title= "{URL}/oauth2/v1/token",
    version= "1.0.0",
    description="API para generar token"
)

app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exeption_handler(request: Request, exc: RequestValidationError):
    folio = uuid.uuid_generate()
    if request.url.path == "/oauth2/v1/token":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({ "folio": folio,"mensaje": "Credenciales requeridas"})
        )
        
    