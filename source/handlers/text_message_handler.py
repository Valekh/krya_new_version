from aiogram import Bot, types, Router

from source.games.game_stories_handler import GameStoriesHandler
from source.services.service_create_chat import ServiceCreateChat
from source.services.service_get_chat import ServiceGetChat
from source.services.service_update_chat import ServiceUpdateChat


class TextMessageHandler:
    def __init__(self,
                 service_get_chat: ServiceGetChat,
                 service_create_chat: ServiceCreateChat,
                 service_update_chat: ServiceUpdateChat,
                 message: types.Message,
                 bot: Bot,
                 router: Router):
        self.service_get_chat = service_get_chat
        self.service_create_chat = service_create_chat
        self.service_update_chat = service_update_chat

        self.message = message
        self.chat_id = message.chat.id
        self.text = message.text

        self.bot = bot
        self.router = router

    async def _check_and_add_chat(self):
        chat = await self.service_get_chat.get(chat_id=self.chat_id)
        if chat is None:
            chat = await self.service_create_chat.create(chat_id=self.chat_id)
        return chat

    async def handle(self):
        chat = await self._check_and_add_chat()
        words = self.text.split()

        if words[1] == "игра":
            if chat.status != "default":
                await self.bot.send_message(self.chat_id, "игра уже идёт!")
                return

            await self.service_update_chat.update_status(chat_id=self.chat_id, status="game")
            await self.bot.send_message(self.chat_id, "набор начался!")
            game = GameStoriesHandler(
                bot=self.bot,
                router=self.router,
                chat_id=self.chat_id,
                service_update_chat=self.service_update_chat
            )
            await game.play(self.message)
