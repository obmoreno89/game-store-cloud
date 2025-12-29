from pydantic import BaseModel, Field

class Result(BaseModel):
   access_token: str = "a1b2c3d4e5f64a7b-8c9d0e1f2a3b4c5d...."
   token_type: str = "bearer"
   
        
        
class Token(BaseModel):
    folio: str  = "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
    mensaje: str = "Operación exitosa"
    resultado: Result 

   