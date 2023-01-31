from typing import Any, Dict, Generic, List, TypeVar
import uuid
from sqlmodel import Session, select
from gilgates_api.models import Model

T = TypeVar("T")


class BaseDAO(Generic[T]):
    cache: Dict[uuid.UUID, T]
    model: T
    session: Session

    def __init__(self, session: Session, schema: Model) -> None:
        """
        The __init__ function is called automatically when a new instance of the class is created.
        It sets up the object with all of the attributes that were defined in its signature.


        :param self: Refer to the instance of the class
        :param table: Table: Specify the table that is being mapped
        :param schema: Model: Define the model that this table is associated with
        :return: Nothing
        :doc-author: Trelent
        """
        self.session = session
        self.model = schema
        self.cache = {}

    async def read(self, ids: List[uuid.UUID]) -> None:
        id_list = [str(a) for a in ids]
        statement = select(self.model).where(self.model.uid in id_list)
        items = self.session.exec(statement)
        for item in items:
            self.cache.update({item.uid: item})

    async def get(self, item_id: uuid.UUID) -> T | None:
        if item_id not in self.cache.keys():
            statement = select(self.model).where(self.model.uid == str(item_id))
            result = self.session.exec(statement).one_or_none()
            if not result:
                return None
            self.cache.update({result.uid: result})
        return self.cache.get(item_id)

    async def delete(self, item_id: uuid.UUID) -> None:
        user = await self.get(item_id)
        if not user:
            return
        self.session.delete(user)
        self.cache.pop(item_id, None)

    async def create(self, item: Model) -> uuid.UUID:
        self.session.add(item)
        self.session.flush([item])
        self.cache.update({item.uid: item})

        return item.uid

    async def update(self, item: Model) -> None:
        self.session.add(item)
        self.session.refresh(item)

    async def get_all(self) -> List[T]:
        statement = select(self.model)
        results = self.session.exec(statement)
        return results.all()

    def clear(self) -> None:
        self.cache = {}

    def commit(self) -> None:
        self.session.commit()

        for item in self.cache.items():
            self.session.flush(item)
