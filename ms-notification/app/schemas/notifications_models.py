from sqlmodel import Field, SQLModel
from datetime import datetime

class NotificationLog(SQLModel):
    id: int = Field(default=None, primary_key=True)
    folio: str = Field(default=None, max_length=36)
    email: str = Field(max_length=50)
    status: str = Field(default="pendiente")
    date_sent: datetime = Field(default_factory=datetime.now)
    
    
class Notification(NotificationLog, table=True):
    __tablename__ = "notification_log"