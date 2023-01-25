from fastapi import status, HTTPException, Depends
from gilgates_api.api import router
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from gilgates_api.context import context
from gilgates_api.services.auth.password import verify_password
from gilgates_api.services.auth.token import create_access_token, create_refresh_token


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

    hashed_pass = str(user.password)
    if not verify_password(form.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }
