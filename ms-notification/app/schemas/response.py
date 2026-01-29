from pydantic import BaseModel, Field
    

class EmailResponse(BaseModel):
    folio: str
    mensaje: str