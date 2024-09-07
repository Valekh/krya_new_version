from source.repositories.chat_repository import ChatRepository

class ServiceGetChat:
    def __init__(self, repository: ChatRepository):
        self.repository = repository

    async def get(self, chat_id: int):
        result = await self.repository.get(chat_id=chat_id)
        return result
