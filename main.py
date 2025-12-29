from fastapi import FastAPI, Request, HTTPException, Depends, Response
from fastapi.security import APIKeyHeader
import httpx
import os

app = FastAPI(title="Api Gateway")
MS_GAMES_URL = os.getenv("MS_GAMES_URL")
MS_TOKEN_URL = os.getenv("MS_TOKEN_URL")

API_KEY_NAME = os.getenv("API_KEY_NAME")
VALID_API_KEY = os.getenv("VALID_API_KEY")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="API Key invalida o ausente")
    return api_key

@app.post("/token")
async def proxy_token(request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{MS_TOKEN_URL.rstrip('/')}/oauth2/v1/token"
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
async def proxy_games(request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{MS_GAMES_URL.rstrip("/")}/game-store/v1/operaciones/juegos"
       
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
            media_type=resp.headers.get("content-type")
        )
