from fastapi import APIRouter, Depends, Query, HTTPException, status, Response
from sqlmodel import Session
from fastapi.security import HTTPBearer
from app.utils.uuid import generat_uuid
from app.db.session import get_session
from app.services.list_games import get_all_games
from app.services.security import get_current_user
from app.schemas.response_models import ResponseGames
from app.api.doc.operations_game import UNAUTHORIZED_RESPONSE

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
    all_games, total_reg, total_pag = get_all_games(session, page)

    if(page > total_pag and total_pag > 0):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    return ResponseGames(
        folio=folio,
        mensaje="Operación Exitosa",
        resultado=all_games,
        total_registros=total_reg,
        total_paginas=total_pag,
        pagina_actual=page
    )