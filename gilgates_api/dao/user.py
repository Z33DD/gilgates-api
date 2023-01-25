from typing import List
from gilgates_api.dao import BaseDAO
from gilgates_api.model.user import user_table, User
from gilgates_api.database import db


class UserDAO(BaseDAO[User]):
    def __init__(self) -> None:
        super().__init__(user_table, User)

    async def get_by_email(self, email: str) -> User | None:
        query = self.table.select().where(self.table.c.email == email)
        result = await db.fetch_one(query)
        if not result:
            return None
        user = User.parse_obj(result)
        return user
