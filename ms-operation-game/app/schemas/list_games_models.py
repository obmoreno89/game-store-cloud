from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict

class ListGameBase(SQLModel):
    name: str = Field(index=True, max_length=200)
    background_image: Optional[str] = None
    rating: Optional[float] = None
    rating_top: int
    price: Optional[int] = Field(default=0)
    current: str
    stock: Optional[int] = Field(default=0)
    sold_out: bool = Field(default=False)
    platforms_xbox_id: int
    platforms_pc_id: int
    platforms_ps_id: int

class ListGameRead(ListGameBase):
    id: int = 3
    name: str = "Halo 3"
    background_image: str = "https://url-image"
    rating: float = 4.32
    rating_top: int = 5
    price: int = 1456
    current: str = "MXN"
    stock: int = 20
    sold_out: bool = False
    platforms_xbox_id: int = 1
    platforms_pc_id: int = 2
    platforms_ps_id: int = 3
    model_config = ConfigDict(from_attributes=True)
    
    
class ListGame(ListGameBase, table=True):
    __tablename__ = "list_game"
    
    id: Optional[int] = Field(default=None, primary_key=True)