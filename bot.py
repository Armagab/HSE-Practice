open_weather_token = "0697516546feabb570ba3df28daca737" # Токен для API погоды

bot_token = "1939186199:AAFjRfOQT2lS2fTOe4m1XSxzmRaz4dKIxfg" # Токен для телеграм бота


import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup

bot = Bot(token=bot_token)
disp = Dispatcher(bot)


@disp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Hello, stranger!")


@disp.message_handler()
async def weather_report(message: types.Message):
    # Добавляю смайлики
    conditions = {
        "Thunderstorm": "Thunderstorm \U000026C8",
        "Drizzle": "Drizzle \U0001F326",
        "Rain": "Rain \U0001F327",
        "Snow": "Snow \U0001F328",
        "Mist": "Mist \U0001F32B",
        "Smoke": "Smoke \U0001F32B",
        "Haze": "Haze \U0001F32B",
        "Dust": "Dust \U0001F32B",
        "Fog": "Fog \U0001F32B",
        "Sand": "Sand \U0001F32B",
        "Ash": "Ash \U0001F32B",
        "Squall": "Squall \U0001F32B",
        "Tornado": "Tornado \U0001F32B",
        "Clear": "Clear \U00002600",
        "Clouds": "Clouds \U00002601"
    }

    try:
        # Делаем запрос
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        # Парсим JSON
        cond = conditions[data["weather"][0]["main"]]
        temp = data["main"]["temp"]
        lvl = ""
        if temp > 0:
            lvl = "+"
        if temp < 0:
            lvl = "-"
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        utc_time = datetime.datetime.utcnow()
        my_time = utc_time + datetime.timedelta(0, data["timezone"])

        # В случае хорошей погоды делаю запрос на Dad Jokes API и вывожу вместе с погодой
        # Тут идет обработка html кода, перевожу его в строку потому что так быстрее
        if cond == "Clear \U00002600" or cond == "Snow \U0001F328":
            q = requests.get("https://icanhazdadjoke.com/")
            soup = BeautifulSoup(q.text, "lxml")
            a = (list(soup.meta.next_siblings))
            string = str(a[19])
            joke = string[15:-29]

            await message.reply(f"Time and Date in {message.text}: {my_time.strftime('%H:%M %d.%m.%Y')}  \n\n"
                                f"{message.text}, weather:\n"
                                f"{cond}\n"
                                f"Temperature: {lvl}{round(temp)}°C\nHumidity: {humidity}%\n"
                                f"Pressure: {pressure} Hpa\nWind speed: {wind_speed} m/s\n\n"
                                f"\U0001F304Sunrise time: {sunrise_time} \n\n"
                                f"\U0001F307Sunset time: {sunset_time}.\n\n\n"
                                f"Looks like it's a good day today,"
                                f" here's a good old dad joke to \t\t\t  "
                                f" keep you up in a good mood! \U00002B07\n\n"
                                f"{joke}")

        else:
            # В случае плохой погоды вывожу факты про Чака Нориса
            # Тут идет обработка html кода, перевожу его в строку потому что так быстрее
            q = requests.get("https://api.chucknorris.io/jokes/random")
            soup = str(BeautifulSoup(q.text, "lxml"))
            ind = soup.find("value")
            string = soup[(ind + 8):-20]

            await message.reply(f"Time and Date in {message.text}: {my_time.strftime('%H:%M %d.%m.%Y')}  \n\n"
                                f"Weather in {message.text}:\n"
                                f"{cond}\n"
                                f"Temperature: {lvl}{round(temp)}°C\nHumidity: {humidity}%\n"
                                f"Pressure: {pressure} Hpa\nWind speed: {wind_speed} m/s\n\n"
                                f"\U0001F304Sunrise time: {sunrise_time} \n\n"
                                f"\U0001F307Sunset time: {sunset_time}.\n\n\n"
                                f"Unfortunately the weather isn't so good here today, "
                                f"but don't get upset! Try to be like Chuck Norris, he never gets upset. "
                                f"By the way here's an interesting fact about him: \U00002B07\n\n"
                                f"{string}")

    # На случай если пользователь опишется/ошибется в названии Города/Страны
    except Exception:
        await message.reply("\U00002757Invalid Input\U00002757")


if __name__ == '__main__':
    executor.start_polling(disp)
