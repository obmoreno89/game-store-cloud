from fastapi import FastAPI, Request, HTTPException, Depends, Response, status
from fastapi.security import APIKeyHeader
import httpx
import os

app = FastAPI(title="Api Gateway", redirect_slashes=False)
IS_PROD = os.getenv("IS_PROD",)
MS_GAMES_URL = os.getenv("MS_GAMES_URL")
MS_GAMES_URL_DEV = os.getenv("MS_GAMES_URL_DEV")
MS_TOKEN_URL = os.getenv("MS_TOKEN_URL")
MS_TOKEN_URL_DEV = os.getenv("MS_TOKEN_URL_DEV")
API_KEY_NAME = os.getenv("API_KEY_NAME")
VALID_API_KEY = os.getenv("VALID_API_KEY")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
   if api_key is None or api_key.strip() == "" or api_key != VALID_API_KEY:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="API key invalida"
       )
   return api_key

@app.post("/token")
async def proxy_token(request: Request):
    async with httpx.AsyncClient() as client:
        url: str
        if IS_PROD == "True":
            url = f"{MS_TOKEN_URL.rstrip('/')}/oauth2/v1/token"
        else: 
            url = f"{MS_TOKEN_URL_DEV.rstrip('/')}/oauth2/v1/token"   
        body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            timeout=60.0
        )
        return Response(
            content=resp.content, 
            status_code=resp.status_code, 
            headers=dict(resp.headers)
        )
    
@app.get("/juegos")
async def proxy_games(request: Request, api_key: str = Depends(verify_api_key)):
    async with httpx.AsyncClient() as client:
       url: str
       if IS_PROD == "True":
            url = f"{MS_GAMES_URL.rstrip('/')}/game-store/v1/operaciones/juegos"
       else:
            url = f"{MS_GAMES_URL_DEV.rstrip('/')}/game-store/v1/operaciones/juegos"    
       
    
       headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
       resp = await client.get(
            url,
            headers=headers,
            params=request.query_params,
            timeout=60.0
        )
       return Response(
            content=resp.content, 
            status_code=resp.status_code, 
            headers=dict(resp.headers)
        )
       
@app.get("/juegos/{game_id}")
async def proxy_games_for_id(request: Request, game_id: int, api_key: str = Depends(verify_api_key)):
    async with httpx.AsyncClient() as client:
       url: str
       if IS_PROD == "True":
            url = f"{MS_GAMES_URL.rstrip('/')}/game-store/v1/operaciones/juegos/{game_id}"
       else:
            url = f"{MS_GAMES_URL_DEV.rstrip('/')}/game-store/v1/operaciones/juegos/{game_id}"    
       
    
       headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
       resp = await client.get(
            url,
            headers=headers,
            params=request.query_params,
            timeout=60.0
        )
       return Response(
            content=resp.content, 
            status_code=resp.status_code, 
            headers=dict(resp.headers)
        )

@app.patch("/juegos/parcial/{game_id}")
async def proxy_games_particial_update(request: Request, game_id: int, api_key: str = Depends(verify_api_key)):
    body = await request.body()
    async with httpx.AsyncClient() as client:
       url: str
       if IS_PROD == "True":
            url = f"{MS_GAMES_URL.rstrip('/')}/game-store/v1/operaciones/juegos/parcial/{game_id}"
       else:
            url = f"{MS_GAMES_URL_DEV.rstrip('/')}/game-store/v1/operaciones/juegos/parcial/{game_id}"    
       
    
       headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
       resp = await client.patch(
            url,
            headers=headers,
            content=body,
            params=request.query_params,
            timeout=60.0
        )
       return Response(
            content=resp.content, 
            status_code=resp.status_code, 
            headers=dict(resp.headers)
        )
       
@app.post("/juegos/crear")
async def proxy_create_games(request: Request, api_key: str = Depends(verify_api_key)):
    body = await request.body()
    async with httpx.AsyncClient() as client:
        if IS_PROD == "True":
             url = f"{MS_GAMES_URL.rstrip('/')}/game-store/v1/operaciones/juegos/crear"
        else:
             url = f"{MS_GAMES_URL_DEV.rstrip('/')}/game-store/v1/operaciones/juegos/crear"
             
        headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
        resp = await client.post(
            url,
            headers=headers,
            content=body,
            params=request._query_params,
            timeout=60.0
        )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers)
        )
  
@app.post("/metodos/pagos")
async def proxy_pay(request: Request, api_key: str = Depends(verify_api_key)):
    body = await request.body()
    pass
                    