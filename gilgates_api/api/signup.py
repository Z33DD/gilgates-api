import uuid
from pydantic import BaseModel, EmailStr, SecretStr
from fastapi import status, HTTPException, APIRouter
from gilgates_api import context
from gilgates_api.model.user import User
from gilgates_api.services.auth.password import hash_password


router = APIRouter()

class UserSignUp(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr


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

    password = hash_password(str(data.password))
    user = User(email=data.email, password=password, name=data.name)
    uid = await dao.user.create(user)

    return UserOut(email=data.email, uid=uid)
