from aiogram import Bot

from source.services.service_create_chat import ServiceCreateChat
from source.services.service_get_chat import ServiceGetChat
from source.services.service_update_chat import ServiceUpdateChat


class TextMessageHandler:
    def __init__(self,
                 service_get_chat: ServiceGetChat,
                 service_create_chat: ServiceCreateChat,
                 service_update_chat: ServiceUpdateChat,
                 chat_id: int,
                 text: str,
                 bot: Bot):
        self.service_get_chat = service_get_chat
        self.service_create_chat = service_create_chat
        self.service_update_chat = service_update_chat
        self.chat_id = chat_id
        self.text= text
        self.bot = bot

    async def _check_and_add_chat(self):
        chat = await self.service_get_chat.get(chat_id=self.chat_id)
        if chat is None:
            chat = await self.service_create_chat.create(chat_id=self.chat_id)
        return chat

    async def handle(self):
        chat = await self._check_and_add_chat()
        words = self.text.split()

        if words[0] == "игра":
            if chat.status != "default":
                await self.bot.send_message(self.chat_id, "игра уже идёт!")
                return

            await self.service_update_chat.update_status(chat_id=self.chat_id, status="game")
            await self.bot.send_message(self.chat_id, "игра началась!")

