import uuid
from gilgates_api.dao import BaseDAO
from gilgates_api.model import User
from sqlmodel import Session, select


class UserDAO(BaseDAO[User]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).one_or_none()
        if not result:
            return None
        self.cache.update({result.uid: result})
        return result
