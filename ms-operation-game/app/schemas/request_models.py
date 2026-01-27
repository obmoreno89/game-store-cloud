from pydantic import BaseModel, Field
from typing import Optional

class GameUpdate(BaseModel):
    stock: Optional[int] = Field(default=None, ge=0)
    isIncrease: bool = False
    name: Optional[str] = Field(default=None, min_length=5, max_length=200)
    background_image: Optional[str] = None
    price: Optional[int] = Field(default=None, ge=100)
    rating: Optional[float] = Field(default=None, ge=0)
    rating_top: Optional[int] = Field(default=None, ge=1)
    current: Optional[str] = Field(default=None, min_length=2, max_length=5)
    platforms_xbox_id: Optional[int] = Field(default=None, ge=1)
    platforms_pc_id: Optional[int] = Field(default=None, ge=1)
    platforms_ps_id: Optional[int] = Field(default=None, ge=1)
    
class GameCreate(BaseModel):
    stock: int = Field(ge=0)
    name: str = Field(min_length=5, max_length=200)
    background_image: str = None
    price: int = Field(ge=100)
    rating: float = Field(ge=0)
    rating_top: int = Field(ge=1)
    current: str = Field(min_length=2, max_length=5)
    platforms_xbox_id: int = Field(ge=1)
    platforms_pc_id: int = Field(ge=1)
    platforms_ps_id: int = Field(ge=1)
    
class ReduceStock(BaseModel):
    stock: int = Field(ge=1)
    
     