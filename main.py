import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers import *
from config import *

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)

    await bot.delete_my_commands()

    commands = [
        BotCommand(command="/start", description="Перезапустить бота 🔁")]
        
    await bot.set_my_commands(commands)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
        