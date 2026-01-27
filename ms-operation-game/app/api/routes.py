import os
from fastapi import APIRouter, Depends, Query, HTTPException, status, Response, Path, Body, Header
from sqlmodel import Session
from fastapi.security import HTTPBearer
from app.utils import generat_uuid
from app.db import get_session
from app.services import get_all_games, get_game_for_id, patch_game, get_current_user, post_game, reduce_stock
from app.schemas import ResponseGames, ResponseGameId, ResponseGameUpdate, GameUpdate, ResponseCreateGame, GameCreate, ReduceStock
from app.api import UNAUTHORIZED_RESPONSE


SECRET_KEY_INTERNAL = os.getenv("SECRET_KEY_INTERNAL")

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
                "folio": folio,
                "mensaje": "Stock insuficiente",
            })
        if game_data.stock == 0:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            "folio": folio,
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

@router.post("/game-store/v1/operaciones/juegos/crear", response_model=ResponseCreateGame, responses=UNAUTHORIZED_RESPONSE, dependencies=[Depends(auth_scheme)])
def create_game(session: Session = Depends(get_session), current_user: dict = Depends(get_current_user), game_data: GameCreate = Body()):
    folio = generat_uuid()
    new_game = post_game(session, game_data)
    
    return ResponseCreateGame(
        folio= folio,
        mensaje= "Operación exitosa"
    )
    
@router.patch("/game-store/v1/operaciones/juegos/reduce-stock/{game_id}")
def reduce_stock_internal(game_id: int, game_data: ReduceStock = Body(), session: Session = Depends(get_session), x_internal_secret: str = Header(None)):
    folio = generat_uuid()
    
    if x_internal_secret != SECRET_KEY_INTERNAL:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"folio": folio, "mensaje": "No estas autorizado"})
    
    game, there_stock = reduce_stock(session, game_id, game_data)
    
    if not there_stock:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    if game.stock is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"folio": folio, "mensaje": "La cantidad del stock es requerida"})
    
    if game.stock < game_data.stock:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"folio": folio, "mensaje": "No hay unidades disponibles"})
    
   
    return ResponseGameUpdate(
        folio=folio,
        mensaje="Operación exitosa",
    )