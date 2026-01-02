from fastapi import APIRouter, Depends, Query, HTTPException, status, Response, Path, Body
from sqlmodel import Session
from fastapi.security import HTTPBearer
from app.utils import generat_uuid
from app.db import get_session
from app.services import get_all_games, get_game_for_id, patch_game, get_current_user
from app.schemas import ResponseGames, ResponseGameId, ResponseGameUpdate, GameUpdate
from app.api import UNAUTHORIZED_RESPONSE

auth_scheme = HTTPBearer()
router = APIRouter(tags=["Operaciones Juegos"])

@router.get("/game-store/v1/operaciones/juegos", response_model=ResponseGames, responses=UNAUTHORIZED_RESPONSE, dependencies=[Depends(auth_scheme)])
def games(session: Session = Depends(get_session), current_user: dict = Depends(get_current_user), page: int = Query(default=1)):
    
    if page <= 0:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                "folio": generat_uuid(),
                "mensaje": "no se admite la página 0",
            })
    
    folio = generat_uuid()
    games, total_reg, total_pag = get_all_games(session, page)

    if(page > total_pag and total_pag > 0):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return ResponseGames(
        folio=folio,
        mensaje="Operación Exitosa",
        resultado=games,
        total_registros=total_reg,
        total_paginas=total_pag,
        pagina_actual=page
    )
    
@router.get("/game-store/v1/operaciones/juegos/{game_id}", response_model=ResponseGameId, responses=UNAUTHORIZED_RESPONSE, dependencies=[Depends(auth_scheme)])
def game_for_id(session: Session = Depends(get_session), current_user: dict = Depends(get_current_user), game_id: int = Path()):
    folio = generat_uuid()
    game =  get_game_for_id(session, game_id)
    
    if game is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return ResponseGameId(
        folio=folio,
        mensaje="Operación Exitosa",
        resultado=game
    )

@router.patch("/game-store/v1/operaciones/juegos/parcial/{game_id}", response_model=ResponseGameUpdate, responses=UNAUTHORIZED_RESPONSE, dependencies=[Depends(auth_scheme)])
def parcial_update(session: Session = Depends(get_session), current_user: dict = Depends(get_current_user), game_id: int = Path(), game_data: GameUpdate = Body()):
    folio = generat_uuid()
    update_game, there_stock = patch_game(session, game_id, game_data)
    
    if update_game is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    if game_data.stock is not None:
        if not there_stock:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                "folio": generat_uuid(),
                "mensaje": "Stock insuficiente",
            })
        if game_data.stock == 0:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "folio": generat_uuid(),
            "mensaje": "no puedes mandar un stock en 0"
        }) 
        if game_data.stock < 0:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "folio": folio,
            "mensaje": "no se permite numeros en negativo"
            })      
    
    return ResponseGameUpdate(
        folio=folio,
        mensaje="Operación exitosa",
    )
        
    