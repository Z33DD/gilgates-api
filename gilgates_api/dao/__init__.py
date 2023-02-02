from typing import Dict, Generic, List, Type, TypeVar
import uuid
from sqlmodel import Session, select
from gilgates_api.model import Model

ModelType = TypeVar("ModelType", bound=Model)


class BaseDAO(Generic[ModelType]):
    needs_commit: bool = False
    cache: Dict[uuid.UUID, ModelType]
    model: ModelType
    db: Session

    def __init__(self, session: Session, model: Type[ModelType]) -> None:
        """
        The __init__ function is called automatically when a new instance of the class is created.
        It sets up the object with all of the attributes that were defined in its signature.


        :param self: Refer to the instance of the class
        :param table: Table: Specify the table that is being mapped
        :param model: Model: Define the model that this table is associated with
        :return: Nothing
        :doc-author: Trelent
        """
        self.db = session
        self.model = model
        self.cache = {}

    async def read(self, ids: List[uuid.UUID]) -> None:
        id_list = [str(a) for a in ids]
        statement = select(self.model).where(self.model.uid in id_list)
        items = self.db.exec(statement)
        for item in items:
            self.cache.update({item.uid: item})

    async def get(self, item_id: uuid.UUID) -> ModelType | None:
        if item_id not in self.cache.keys():
            statement = select(self.model).where(self.model.uid == str(item_id))
            result = self.db.exec(statement).one_or_none()
            if not result:
                return None
            self.cache.update({result.uid: result})
        return self.cache.get(item_id)

    async def delete(self, item_id: uuid.UUID) -> None:
        user = await self.get(item_id)
        if not user:
            return
        self.db.delete(user)
        self.cache.pop(item_id, None)
        self.needs_commit = True

    async def create(self, item: Model) -> uuid.UUID:
        self.db.add(item)
        self.db.flush([item])
        self.cache.update({item.uid: item})
        self.needs_commit = True

        return item.uid

    async def update(self, item: Model) -> None:
        self.db.add(item)
        self.needs_commit = True

    async def get_all(self) -> List[ModelType]:
        statement = select(self.model)
        results = self.db.exec(statement)
        return results.all()

    def clear(self) -> None:
        self.cache = {}

    def commit(self, force: bool = False) -> None:
        if not self.needs_commit and not force:
            return

        self.db.commit()

        for item in self.cache.items():
            self.db.flush(item)
