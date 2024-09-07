from aiogram import Bot

from source.repositories.bot_speech_repository import BotSpeechRepository

class GetBotSpeechService:
    def __init__(self,
                 repository: BotSpeechRepository,
                 bot: Bot,
                 chat_id: int):
        self.repository = repository
        self.bot = bot
        self.chat_id = chat_id

    async def greetings(self):
        greetings = await self.repository.read_one(keyword="greetings")
        await self.bot.send_photo(self.chat_id,
                                  caption=greetings.text,
                                  photo=greetings.image)
