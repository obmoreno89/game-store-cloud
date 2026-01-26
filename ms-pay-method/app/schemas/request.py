from pydantic import BaseModel, Field

class RequestOrderPay(BaseModel):
    name: str = Field(index=True, max_length=200)
    user_id: int = Field(index=True, ge=1)
    unit: int = Field(ge=1)
    platforms_id: int = Field(ge=1)
    price: int = Field(ge=100)
    game_id: int = Field(ge=1)
    