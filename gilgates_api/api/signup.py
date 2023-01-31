import uuid
from pydantic import BaseModel, EmailStr
from fastapi import status, HTTPException, APIRouter, Depends
from sqlmodel import Session
from gilgates_api.dao_factory import dao_factory
from gilgates_api.deps import get_session
from gilgates_api.models import User
from gilgates_api.services.auth.password import hash_password


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

    return UserOut(email=data.email, uid=uid)
