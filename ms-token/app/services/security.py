import jwt
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils import uuid


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
except ValueError:
    print ("no es un numero valido")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
if not SECRET_KEY:
    raise ValueError("No se encontro la llave seguridad")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "sub": data.get("username")})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    folio = uuid.uuid_generate()
    credentials_exeption = JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder({ "Folio": folio,"Mensaje": "Credenciales incorrectas"}),
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exeption
        
        return username
    
    except jwt.ExpiredSignatureError:
        return JSONResponse(
             status_code=status.HTTP_401_UNAUTHORIZED,
             content=jsonable_encoder({ "Folio": folio,"Mensaje": "Token expirado"}),
             headers={"WWW-Authenticate": "Bearer"},
        )
    
    except jwt.InvalidTokenError:
        raise credentials_exeption
        
