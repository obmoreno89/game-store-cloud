from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer 
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.db import engine
from app.utils import generat_uuid
from app.schemas import OrderPay

security = HTTPBearer()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    
    yield
    
    print("Limpiando recurso")

app = FastAPI(title="{URL}/game-store/v1/metodos/pagos", version= "1.0.0",
    description="API para generar metodo de pago", swagger_ui_parameters={"operationsSorter": "method"},
    lifespan=lifespan, 
    openapi_url="/openapi.json",
    docs_url="/docs")

@app.exception_handler(HTTPException)
async def custom_http_exeption_handler(request: Request, exc: HTTPException):
    folio = generat_uuid()
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
            headers=exc.headers
        )
        
    return JSONResponse(
        status_code=exc.status_code,
        content={"folio": folio, "mensaje": str(exc.detail)},
        headers=exc.headers
    )
    
#app.include_router(router)
    

    
