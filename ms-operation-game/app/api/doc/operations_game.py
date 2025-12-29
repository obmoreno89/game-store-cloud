from starlette import status
from typing import Dict, Any


UNAUTHORIZED_RESPONSE: Dict[int, Dict[str, Any]] = {
     status.HTTP_204_NO_CONTENT: {
        "description": "Sin contenido la pagina",
         "content": {
            "application/json": {
    
            }
        }
    },
    
    status.HTTP_400_BAD_REQUEST: {
        "description": "Pagina con valor 0",
         "content": {
            "application/json": {
                "example": {
                    "folio": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
                    "mensaje": "No se admite la página 0"
                }
            }
        }
    },
    
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Token no cumple la estructura o token expirado",
        "content": {
            "application/json": {
                "example": {
                    "folio": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
                    "mensaje": "Token expirado o malformado"
                }
            }
        }
    }
}