import uuid
from pydantic import BaseModel, EmailStr
from fastapi import status, HTTPException, APIRouter, Depends
from sqlmodel import Session
from gilgates_api.dao_factory import dao_factory
from gilgates_api.deps import get_session
from gilgates_api.model import User
from gilgates_api.services.auth.password import hash_password
from gilgates_api.tasks import send_email


router = APIRouter()


class UserSignUp(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: EmailStr
    uid: uuid.UUID


@router.post("/signup", summary="Create new user", response_model=UserOut)
async def create_user(data: UserSignUp, session: Session = Depends(get_session)):
    # querying database to check if user already exist
    dao = dao_factory(session)
    user = await dao.user.get_by_email(data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )

    user = User(email=data.email, name=data.name)
    user.password = hash_password(data.password)
    uid = await dao.user.create(user)
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

    return UserOut(email=data.email, uid=uid)
