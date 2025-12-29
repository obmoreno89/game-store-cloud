from fastapi import FastAPI, Request
from sqlmodel import SQLModel
from app.db.session import engine
from app.api.routes import router
from app.schemas.list_games_models import ListGame
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.utils.uuid import generat_uuid
from fastapi.security import HTTPBearer

security = HTTPBearer()

app = FastAPI(title="{URL}/game-store/v1/operaciones/juegos", version= "1.0.0",
    description="API para hacer operaciones nivel CRUD", swagger_ui_parameters={"operationsSorter": "method"}, root_path="/juegos", 
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

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    
app.include_router(router)


