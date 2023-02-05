from typing import List
from fastapi import Depends, APIRouter, Query
from sqlmodel import Session
from gilgates_api.deps import current_user, get_session
from gilgates_api.model import User
from gilgates_api import dao_factory


router = APIRouter()


@router.get(
    "/me",
    summary="Get details of currently logged in user",
    response_model=User,
)
async def get_me(user: User = Depends(current_user)):
    return user


@router.get(
    "/",
    summary="Get all users",
    response_model=List[User],
)
async def get_all_users(
    offset: int = 0, 
    limit: int = Query(default=100, lte=100),
    user: User = Depends(current_user), 
    session: Session = Depends(get_session),
):
    dao = dao_factory(session)
    users = dao.user.get_all(limit, offset)
    return users
