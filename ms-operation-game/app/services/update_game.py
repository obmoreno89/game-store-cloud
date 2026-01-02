from sqlmodel import Session, select
from app.schemas.list_games_models import ListGame
from fastapi import Body
from app.schemas import GameUpdate


def patch_game(session:Session, game_id: int, game_data: GameUpdate = Body()):
    statement = select(ListGame).where(ListGame.id == game_id)
    game = session.exec(statement).first()
    thereStock: bool = True
    
    if not game:
        return None, False
    
    if not game_data.isIncrease:
        if game_data.stock > game.stock:
            thereStock = False
            return game, thereStock
        game.stock -= game_data.stock
    else:
        game.stock += game_data.stock
        game.sold_out = False
    
    if game.stock == 0:
        game.sold_out = True 
    else:
        game.sold_out = False       
        
    session.add(game)
    session.commit()
    session.refresh(game)
    
    return game, thereStock
    
    