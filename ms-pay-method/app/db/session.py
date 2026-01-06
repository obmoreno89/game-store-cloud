import os
from sqlmodel import create_engine, Session
from typing import Generator
from dotenv import load_dotenv
load_dotenv()

IS_PROD = os.getenv("IS_PROD", "false").lower() == "true"
IS_RENDER = os.getenv("RENDER") is not None
IS_STRICKLY_PROD = IS_PROD or IS_RENDER

if IS_STRICKLY_PROD:
    base_url = os.getenv("DATABASE_URL")
    connect_args = {"sslmode": "require"}
else:
    base_url = os.getenv("DATABASE_URL_DEV")
    connect_args = {}
    
if not base_url:
     raise ValueError(f"Error: URL de base de datos no encontrada para {'PROD' if IS_STRICKLY_PROD else 'DEV'}")

if base_url.startswith("postgres://"):
    final_url = base_url.replace("postgres://", "postgresql://", 1)
else:
    final_url = base_url

engine = create_engine(
    final_url,
    echo=not IS_STRICKLY_PROD,
    connect_args=connect_args
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
