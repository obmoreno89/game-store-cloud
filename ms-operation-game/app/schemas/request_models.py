from pydantic import BaseModel
from typing import Optional

class GameUpdate(BaseModel):
    stock: int
    isIncrease: bool 