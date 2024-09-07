from abc import ABC, abstractmethod
from inspect import Traceback
from typing import Type

from source.repositories.bot_speech_repository import BotSpeechRepository


class AbstractRepositoryManager(ABC):
    _auto_commit: bool = False

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...

    async def __aenter__(self):
        pass

    async def __aexit__(
            self, exc_type: Type[Exception], exc_val: Exception, exc_tb: Traceback
    ) -> None:
        if exc_val:
            await self.rollback()
        else:
            await self.commit()
        await self.close()

    async def get_bot_speech_repository(self) -> BotSpeechRepository: ...