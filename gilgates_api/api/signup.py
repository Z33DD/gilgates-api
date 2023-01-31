import uuid
from pydantic import BaseModel, EmailStr
from fastapi import status, HTTPException, APIRouter
from gilgates_api import context
from gilgates_api.model.user import User
from gilgates_api.services.auth.password import hash_password
from gilgates_api.tasks.email import send_email


router = APIRouter()

class UserSignUp(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: EmailStr
    uid: uuid.UUID


@router.post("/signup", summary="Create new user", response_model=UserOut)
async def create_user(data: UserSignUp):
    # querying database to check if user already exist
    dao = context.get()
    user = await dao.user.get_by_email(data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )

    user = User(email=data.email, name=data.name)
    user.password = hash_password(data.password)
    uid = await dao.user.create(user)
    send_email.delay(user.email)

    return UserOut(email=data.email, uid=uid)
