from aiogram import Bot,Dispatcher
from dotenv import load_dotenv 
import asyncio
import os
from handlers.finder import router,weather_info
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
import logging

log = logging.getLogger(__name__)

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

async def main():
    if TOKEN and API_KEY:
        bot = Bot(token = TOKEN)
        dp = Dispatcher()
        dp.include_routers(router)
        scheduler = AsyncIOScheduler(timezone = "Asia/Qyzylorda")
        params = {"lat":45.6167,
                  "lon":63.3167,
                  "appid":API_KEY,
                  "units":"metric"}
        
        async with aiohttp.ClientSession() as session:
            log.info("Сессия запущена")
            scheduler.add_job(func = weather_info,
                              trigger = "cron",
                              kwargs = {
                                  "bot":bot,
                                  "chat_id":8223796770,
                                  "session":session,
                                  "params":params,
                                  "intro":"Добрый день"
                                       },
                              id = "Good day",
                              hour = 9,
                              minute = 10)
            try:
                log.info("Планировщик и бот запущены")
                scheduler.start()
                await dp.start_polling(bot)
            except Exception as e:
                log.error(e)
            finally:
                log.info("Все приостановленно")
                await bot.session.close()
                if scheduler.running:
                    scheduler.shutdown(wait = False)

if __name__ == "__main__":
    asyncio.run(main())
