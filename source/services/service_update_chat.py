from source.repositories.chat_repository import ChatRepository

class ServiceUpdateChat:
    def __init__(self, repository: ChatRepository):
        self.repository = repository

    async def update_status(self, chat_id: int, status: str):
        result = await self.repository.update(
            chat_id=chat_id,
            status=status
        )
        return result