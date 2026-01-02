from sqlmodel import Session, select
from typing import List, Optional
from app.schemas import ListGame

def get_game_for_id(session: Session, game_id: int) -> Optional[ListGame]:
    statement = select(ListGame).where(ListGame.id == game_id)
    game = session.exec(statement).first()
    return game
