from pydantic import BaseModel

class Result(BaseModel):
    url: str

class OrderPayResponse(BaseModel):
    folio: str
    mensaje: str
    resultado: Result