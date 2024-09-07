from source.repositories.chat_repository import ChatRepository

class ServiceCreateChat:
    def __init__(self, repository: ChatRepository):
        self.repository = repository

    async def create(self, chat_id: int):
        result = await self.repository.create(
            chat_id=chat_id,
            status="default"
        )
        return result
