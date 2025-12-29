from sqlmodel import Session, select
from sqlalchemy import func
import math
from typing import List
from app.schemas.list_games_models import ListGame



def get_all_games(session: Session, page: int) -> List[ListGame]:
    PAGE_SIZE = 10
    
    total_query = select(func.count()).select_from(ListGame)
    total_register = session.exec(total_query).one()
    total_page = math.ceil(total_register / PAGE_SIZE)
    skip = (page - 1) * PAGE_SIZE
    statement = select(ListGame).offset(skip).limit(PAGE_SIZE)
    
    games = session.exec(statement).all()
    
    return games, total_register, total_page