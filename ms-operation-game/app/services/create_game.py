from sqlmodel import Session, select
from app.schemas import ListGame, GameCreate
from fastapi import Body, HTTPException, status
from app.utils import generat_uuid

def post_game(session:Session, game_data: GameCreate = Body()):
    statement = select(ListGame).where(ListGame.name == game_data.name)
    existing_game = session.exec(statement).first()
    folio = generat_uuid()
    
    if existing_game:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail={
                "folio": folio,
                "mensaje": "El juego ya existe"
            }
        )


    new_game = ListGame.model_validate(game_data)
    session.add(new_game)
    
    
    try:
        session.commit()
        session.refresh(new_game)
        return new_game
    except Exception as e:
        session.rollback()
        raise e    
    
    