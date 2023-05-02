import uuid
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends
from sqlmodel import Session
from gilgates_api import dao_factory
from gilgates_api.deps import get_session
from gilgates_api.services.user.new_user import create_new_user


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
    dao = dao_factory(session)
    uid = await create_new_user(
        dao, name=data.name, email=data.email, password=data.password
    )

    dao.commit()

    return UserOut(email=data.email, uid=uid)
