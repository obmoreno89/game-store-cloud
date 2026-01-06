from sqlmodel import Field, SQLModel

class Order(SQLModel):
    folio: str = Field(primary_key=True)
    name: str = Field(index=True, max_length=200)
    unit: int
    platforms_id: int
    price: int
    status: str

class OrderPay(Order, table=True):
    __tablename__ = "order_pay"
    
    
    