import asyncio
from curses.ascii import isdigit

from aiogram import Bot, types, Router, F

from source.services.service_update_chat import ServiceUpdateChat


class GameStoriesHandler:
    def __init__(self,
                 bot: Bot,
                 router: Router,
                 chat_id: int,
                 service_update_chat: ServiceUpdateChat):
        self.bot = bot
        self.router = router
        self.chat_id = chat_id
        self.service_update_chat = service_update_chat
        self.players = {}

    async def recruitment(self, start_player_msg: types.Message):
        queue = asyncio.Queue()
        self.players = {
            start_player_msg.from_user.id: start_player_msg.from_user.first_name
        }

        async def get_message_in_queue(message: types.Message) -> None:
            await queue.put(message)

        async def handle_message():
            while True:
                message = await queue.get()
                words = message.text.lower().split()
                if words[0] in ('вступить', 'играть', 'войти', 'зайти') or \
                        message.text.lower() == "игра хочу играт":

                    if message.from_user.id in self.players:
                        answer = "ты уже в участниках!"
                    else:
                        self.players[message.from_user.id] = message.from_user.first_name
                        answer = "ты вступил в игру!"

                    await message.reply(answer)

                elif words[0] in ("игроки", "участники", "отряд"):
                    if len(self.players) < 1:
                        answer = "игроков нет!"
                    else:
                        answer = "в отряде:\n"
                        for player_id, username in self.players.items():
                            answer += f"{username}; "
                    await message.reply(answer)
                elif words[0] in ('начать', "впирёд!"):
                    if message.from_user.id == start_player_msg.from_user.id:
                        queue.task_done()
                        return
                    else:
                        await self.bot.send_message(self.chat_id, "ти не можеш начать игру!😡")

                queue.task_done()

        self.router.message.register(get_message_in_queue, F.chat.id == self.chat_id)
        try:
            await asyncio.wait_for(handle_message(), timeout=30)
            await self.bot.send_message(self.chat_id, "ти смог начать игру")
        except asyncio.TimeoutError:
            await self.bot.send_message(self.chat_id, "время вышло и всё токое")
        finally:
            self.router.message.handlers.pop()
            await self.bot.send_message(self.chat_id, "игроем")

        return self.players

    async def ask_question(self):
        queue = asyncio.Queue()
        async def get_message_in_queue(message: types.Message) -> None:
            await queue.put(message)

        async def get_answer():
            await queue.get()
            queue.task_done()

        await self.bot.send_message(self.chat_id, "прозвучал вопрос")
        await asyncio.sleep(3.5)
        await self.bot.send_message(self.chat_id, "типа вопрос")
        await asyncio.sleep(1.5)
        for player_id, username in self.players.items():
            await self.bot.send_message(self.chat_id, f"отвечает {username} (30 сек.)")
            self.router.message.register(get_message_in_queue, F.from_user.id == player_id)
            try:
                await asyncio.wait_for(get_answer(), timeout=30)
                await self.bot.send_message(self.chat_id, "ответ принят")
            except asyncio.TimeoutError:
                await self.bot.send_message(self.chat_id, "время на ответ вышло и всё токое")
            finally:
                self.router.message.handlers.pop()
                await asyncio.sleep(1.5)
                continue

    async def voting_to_kick(self):
        queue = asyncio.Queue()
        async def get_message_in_queue(message: types.Message) -> None:
            await queue.put(message)

        async def voting():
            while True:
                message = await queue.get()
                if not message.text.isdigit() or int(message.text) > len(votes):
                    queue.task_done()
                    continue
                votes[int(message.text) - 1][1] += 1
                break


        list_to_vote = "в палату зашёл глав. врач! шизоидам нужно выбрать кого ему отдать (20 сек.):\n"
        votes = []
        for index, (player_id, username) in enumerate(self.players.items()):
            list_to_vote += f"{index + 1}. {username}\n"
            votes.append([player_id, 0])
        await self.bot.send_message(self.chat_id, list_to_vote)

        self.router.message.register(get_message_in_queue, F.chat.id == self.chat_id)
        try:
            await asyncio.wait_for(voting(), timeout=20)
            await self.bot.send_message(self.chat_id, "все проголосовали!")
        except asyncio.TimeoutError:
            await self.bot.send_message(self.chat_id, "время голосования вышло, глав. врач теряет терпение")
        finally:
            self.router.message.handlers.pop()
            await asyncio.sleep(2)

            results = "результаты:\n"
            for index, (player_id, votes_int) in enumerate(votes):
                results += f"{index + 1}. {self.players[player_id]}: {votes_int }\n"
            await self.bot.send_message(self.chat_id, results)
            await self.bot.send_message(self.chat_id, "голосование окончено")


    async def play(self, start_player_msg: types.Message):
        players = await self.recruitment(start_player_msg)

        if len(players) < 1:
            message = "не набралось 4 человека, игра отменена!"
            await self.bot.send_message(self.chat_id, message)
            await self.service_update_chat.update_status(self.chat_id, "default")
            return

        while True:
            await self.ask_question()

            # if len(self.players) < 4:
            #     break

            await self.voting_to_kick()
