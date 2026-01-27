from sqlmodel import Field, SQLModel
from datetime import datetime

class Order(SQLModel):
    user_id: int = Field(index=True)
    game_id: int
    folio: str = Field(primary_key=True)
    name: str = Field(index=True, max_length=200)
    unit: int
    platforms_id: int
    price: int
    status: str
    date_order_create: datetime = Field(default_factory=datetime.now)
    date_order_pay: datetime | None = Field(default=None)

class OrderPay(Order, table=True):
    __tablename__ = "order_pay"
    
    
    