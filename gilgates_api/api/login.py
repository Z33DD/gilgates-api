from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from gilgates_api import context
from gilgates_api.services.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
)
from gilgates_api.tasks import send_email


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


class ResendWelcomeEmailSchema(BaseModel):
    email: EmailStr


@router.post(
    "/resend_welcome_email",
    summary="Resent the welcome email to the customer",
)
async def resend_welcome_email(data: ResendWelcomeEmailSchema):
    dao = context.get()
    user = await dao.user.get_by_email(data.email)

    if user is None or user.password is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or user already set password",
        )
    send_email.delay(
        user.email,
        "welcome",
        {
            "product_url": "product_url_Value",
            "product_name": "GilGates",
            "name": user.name,
            "action_url": "action_url_Value",
            "login_url": "login_url_Value",
            "username": user.email,
            "trial_length": "trial_length_Value",
            "trial_start_date": "trial_start_date_Value",
            "trial_end_date": "trial_end_date_Value",
            "support_email": "support_email_Value",
            "live_chat_url": "live_chat_url_Value",
            "sender_name": "sender_name_Value",
            "help_url": "help_url_Value",
            "company_name": "Codetta Tech",
            "company_address": "https://codetta.tech",
        },
    )

    return {"message": "Email sent"}
