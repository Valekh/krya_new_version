import asyncio
from os import getenv

from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberUpdated
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, Router, F

from source.handlers.text_message_handler import TextMessageHandler
from source.repositories.manager import orm_repository_manager_factory
from source.services.service_create_chat import ServiceCreateChat
from source.services.service_get_bot_speech import GetBotSpeechService
from source.services.service_get_chat import ServiceGetChat
from source.services.service_update_chat import ServiceUpdateChat

load_dotenv()

bot = Bot(token=getenv("API_TOKEN"))
dp = Dispatcher(bot=bot)
router = Router()


async def text_message(message: types.Message):
    if message.content_type != types.ContentType.TEXT:
        return

    repository_manager = orm_repository_manager_factory()
    async with repository_manager:
        handler = TextMessageHandler(
            service_get_chat=ServiceGetChat(
                repository=repository_manager.get_chat_repository()
            ),
            service_create_chat=ServiceCreateChat(
                repository=repository_manager.get_chat_repository()
            ),
            service_update_chat=ServiceUpdateChat(
                repository=repository_manager.get_chat_repository()
            ),
            message=message,
            bot=bot,
            router=router
        )
        await handler.handle()


async def bot_added_to_chat(event: ChatMemberUpdated):
    if event.new_chat_member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR] \
            or event.old_chat_member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
        return

    repository_manager = orm_repository_manager_factory()
    async with repository_manager:
        service = GetBotSpeechService(
            repository_manager.get_bot_speech_repository(),
            bot,
            event.chat.id
        )
        await service.greetings()

async def get_message(message: types.Message) -> None:
    await message.reply("сообщение после добавления")


async def main():
    router.message.register(text_message, F.text.startswith("кря "))
    dp.include_router(router)

    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
