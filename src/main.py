import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, ADMIN_ID
from handlers import router

async def on_startup(bot: Bot):
    await bot.send_message(ADMIN_ID, "Бот запущен")

async def on_shutdown(bot: Bot):
    await bot.send_message(ADMIN_ID, "Бот остановлен")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await on_startup(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(bot)
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())