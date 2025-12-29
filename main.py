from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
import httpx
import os

app = FastAPI("Api Gateway")
MS_GAMES_URL = os.getenv("MS_GAMES_URL")
MS_TOKEN_URL = os.getenv("MS_TOKEN_URL")

API_KEY_NAME = os.getenv("API_KEY_NAME")
VALID_API_KEY = os.getenv("VALID_API_KEY")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="API Key invalida o ausente")
    return api_key

@app.api_route("/token/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_token(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{MS_TOKEN_URL}/{path}"
        resp = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            content=await request.body()
        )
        return resp.json()
    
@app.api_route("/juegos/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_games(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{MS_GAMES_URL}/{path}"
        resp = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            content=await request.body()
        )
        return resp
