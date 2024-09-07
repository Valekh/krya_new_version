from sqlalchemy.ext.asyncio import AsyncSession

from .absract_manager import AbstractRepositoryManager
from .bot_speech_repository import BotSpeechRepository
from .chat_repository import ChatRepository
from ..db_manager import session_factory


class OrmRepositoryManager(AbstractRepositoryManager):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def close(self) -> None:
        await self._session.close()

    def get_bot_speech_repository(self) -> BotSpeechRepository:
        return BotSpeechRepository(self._session)

    def get_chat_repository(self) -> ChatRepository:
        return ChatRepository(self._session)

def orm_repository_manager_factory() -> OrmRepositoryManager:
    return OrmRepositoryManager(session_factory())