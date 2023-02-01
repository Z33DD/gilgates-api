from fastapi import Depends, APIRouter
from gilgates_api import context
from gilgates_api.model import User
from gilgates_api.deps import current_user

router = APIRouter()


@router.get(
    "/user/me",
    summary="Get details of currently logged in user",
    response_model=User,
)
async def get_me(user: User = Depends(current_user)):
    return user
