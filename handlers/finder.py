from aiogram import Router,F,Bot
from aiogram.types import Message
import asyncio
import aiohttp
import logging
from utils.weather_formatter import weather_formatter

log = logging.getLogger(__name__)

router = Router()

async def weather_info(bot:Bot,session:aiohttp.ClientSession,params:dict,chat_id:int=None,intro:str="Здраствуйте"):
        try:
            async with session.get("https://api.openweathermap.org/data/2.5/weather",params = params) as response:
                response.raise_for_status()
                data = await response.json()
                if not data:
                    log.warning("Прогноз не был найден!")
                    await bot.send_message(chat_id = chat_id,text = "Извините прогноз не найден :(")
                    return
                main = data.get("main",{})
                wind = data.get("wind",{})
                api_data = {"temp":main.get("temp",None),
                            "wind_speed":wind.get("speed",None),
                            "humidity":main.get("humidity",None)}                
                letter = weather_formatter(intro,api_data)
                await bot.send_message(chat_id = chat_id,text = letter)
        except Exception as e:
            log.error(e)
            await bot.send_message(chat_id = chat_id,text = "Произошли неполадки :(")
                