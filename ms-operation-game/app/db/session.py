from sqlmodel import create_engine, Session
from dotenv import load_dotenv
load_dotenv()
from typing import Generator
import os

DATABASE_URL = os.environ["DATABASE_URL"]

if not DATABASE_URL:
    raise ValueError("La variable data baseno esta definida en la variable de entorno")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True, connect_args={"sslmode": "require"})

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session