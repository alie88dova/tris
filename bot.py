import asyncio
import aiosqlite

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from dotenv import dotenv_values


dp = Dispatcher()


#команда старт
@dp.message(CommandStart())
async def check_user_id(message: types.Message):
    if not await get_user(message.from_user.id):
        await message.reply("У вас нет доступа к этому боту.")
        return
    await message.reply("Добро пожаловать!")

#база данных


async def add_user(user_id: int):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT user_id FROM users",) as cursor:
            users = await cursor.fetchall()
            users = [x[0] for x in users]
            print(users)
            if users is None:
                return False

            return user_id in users

#добавление в бд для доступа
@dp.message(Command("add"))
async def add_sw(message: types.Message):
   if message.from_user.id == 431862198:
       user_id = message.text.split()[1]
       print (user_id)
       await add_user(int(user_id))
       await message.reply(f"Пользователь {user_id} добавлен")

#запуск бота
async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    token=dotenv_values(".env")
    bot = Bot(token=token["token"])

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())