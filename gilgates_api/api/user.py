from fastapi import Depends, APIRouter
from gilgates_api.deps import current_user
from gilgates_api.model import User


router = APIRouter()


@router.get(
    "/me",
    summary="Get details of currently logged in user",
    response_model=User,
)
async def get_me(user: User = Depends(current_user)):
    return user
