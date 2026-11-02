import asyncio, logging, sys
from aiogram import Bot, Dispatcher
from bot_sys.handlers import router as MVP_router
from bot_sys.antiflood import router as garbage_router
from bot_sys.direction_handler import router as direct_router
from bot_sys.errors import error_handler
from config import BOT_TOKEN

TOKEN = BOT_TOKEN       

logging.basicConfig(level = logging.INFO, stream = sys.stdout)

async def main():
    bot = Bot(token = TOKEN)
    dp = Dispatcher()
    dp.errors.register(error_handler)
    dp.include_routers(MVP_router, direct_router, garbage_router)
    logging.info('Попытка запуска бота')
    await dp.start_polling(bot)

if __name__ == '__main__': 
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('stop')
