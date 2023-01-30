from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from gilgates_api import context
from gilgates_api.services.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter()


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


@router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    dao = context.get()
    user = await dao.user.get_by_email(form.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User don't have a password",
        )

    if not verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }
