from contextlib import suppress
import sqlalchemy.exc
from sqlalchemy import update

from .abstract_repository import AbstractRepository
from source.models import Chat


class ChatRepository(AbstractRepository[Chat]):
    _model = Chat

    async def get(self, **kwargs) -> _model | None:
        with suppress(sqlalchemy.exc.NoResultFound):
            result = await self.read_one(**kwargs)
            return result

    async def update(self, chat_id: int, **kwargs) -> None:
        query = update(self._model).where(self._model.chat_id == chat_id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
