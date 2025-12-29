from starlette import status
from typing import Dict, Any


UNAUTHORIZED_RESPONSE: Dict[int, Dict[str, Any]] = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "Credenciales requeridas",
         "content": {
            "application/json": {
                "example": {
                    "folio": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
                    "mensaje": "Las credenciales son requeridas"
                }
            }
        }
    },
    
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Credenciales inválidas o Autenticación fallida.",
        "content": {
            "application/json": {
                "example": {
                    "folio": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
                    "mensaje": "credenciales incorrectas"
                }
            }
        }
    }
}