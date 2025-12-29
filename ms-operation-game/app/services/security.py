from fastapi.security import OAuth2
from fastapi import Request, status, Depends, HTTPException
from typing import Optional, Any
import jwt
from jwt.exceptions import PyJWTError
import os

try:
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.environ["ALGORITHM"]
except KeyError:
    raise ValueError("No se encontraron las variables")

oauth2_scheme = OAuth2(auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    token = token.strip()
    
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
    
    if not token:
       raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token es requerido",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token incompleto, falta el identificador (sub)",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
            
            
    except PyJWTError as e:
        print(f"--- ERROR DE VALIDACIÓN ---: {type(e).__name__} - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado o malformado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {"user_id": user_id}