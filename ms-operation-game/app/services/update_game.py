from sqlmodel import Session, select
from app.schemas import ListGame, GameUpdate
from fastapi import Body



def patch_game(session:Session, game_id: int, game_data: GameUpdate = Body()):
    statement = select(ListGame).where(ListGame.id == game_id)
    game = session.exec(statement).first()
    there_stock: bool = True
    
    if not game:
        return None, False
    
    update_data = game_data.model_dump(exclude_unset=True, exclude={"stock", "isIncrease"})
    game.sqlmodel_update(update_data)
    
    if game_data.stock is not None:
        if not game_data.isIncrease:
            if game_data.stock > game.stock:
                there_stock = False
                return game, there_stock
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
    
    return game, there_stock
    
    