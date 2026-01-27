from sqlmodel import Session, select
from app.schemas import ListGame, ReduceStock
from fastapi import Body

def reduce_stock(session: Session, game_id: int, game_data: ReduceStock = Body()):
    statement = select(ListGame).where(ListGame.id == game_id)
    game = session.exec(statement).first()
    there_stock: bool = True
    
    if not game:
        return None, False
    
    if game.stock < game_data.stock:
        return game, False
    
    game.stock -= game_data.stock
    
    if game.stock == 0:
        game.sold_out = True
    else: 
        game.sold_out = False
        
    session.add(game)
    session.commit()
    session.refresh(game)
    
    return game, there_stock
        