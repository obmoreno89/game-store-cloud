from pydantic import BaseModel, EmailStr, Field

class EmailRequest(BaseModel):
    folio: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    game_name: str = Field(max_length=100)
    
    
    
    