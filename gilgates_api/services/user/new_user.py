import uuid
from pydantic import EmailStr
from fastapi import status, HTTPException
from gilgates_api.model import User
from gilgates_api.tasks import send_email
from gilgates_api.services.auth import hash_password
from gilgates_api.dao_factory import MasterDAO


async def create_new_user(
    dao: MasterDAO, name: str, email: EmailStr, password: str
) -> uuid.UUID:
    user = await dao.user.get_by_email(email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )

    user = User(email=email, name=name)
    user.password = hash_password(password)
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

    return uid
