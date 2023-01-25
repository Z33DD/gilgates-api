import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from gilgates_api.context import context
from gilgates_api.model.user import User

from gilgates_api.services.auth.token import verify_token


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


async def current_user(token: str = Depends(reuseable_oauth)) -> User:
    dao = context.get()
    claims = verify_token(token)
    user_id = uuid.UUID(claims.sub)

    user: User| None = await dao.user.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
