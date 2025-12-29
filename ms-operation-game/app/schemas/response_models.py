from typing import List 
from pydantic import BaseModel
from app.schemas.list_games_models import ListGameRead

class ResponseGames(BaseModel):
    folio: str = "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
    mensaje: str = "Operación exitosa"
    resultado: List[ListGameRead]
    total_registros: int = 20
    total_paginas: int = 2
    pagina_actual: int = 1
    