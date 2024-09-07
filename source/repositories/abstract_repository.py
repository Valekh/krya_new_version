from abc import ABC
from typing import TypeVar, Type, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Generic

_MODEL_TYPE = TypeVar("_MODEL_TYPE")


class AbstractRepository(ABC, Generic[_MODEL_TYPE]):
    _model: Type[_MODEL_TYPE] | None =None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> _MODEL_TYPE:
        entity = self._model(**kwargs)
        self.session.add(entity)
        await self.session.flush([entity])
        await self.session.refresh(entity)
        return entity

    async def read(self, **kwargs) -> Sequence[_MODEL_TYPE]:
        result = await self.session.execute(
            select(self._model).filter_by(**kwargs)
        )
        entities = result.scalars().all()
        return entities

    async def read_one(self, **kwargs) -> _MODEL_TYPE:
        result = await self.session.execute(
            select(self._model).filter_by(**kwargs).limit(1)
        )
        entity = result.scalars().one()
        return entity

    async def update(self, entity_id: int, **kwargs) -> None:
        update(self._model).where(self._model.id == entity_id).values(**kwargs)
        await self.session.commit()
