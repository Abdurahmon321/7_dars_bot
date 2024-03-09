from telebot.types import Message
from data.loader import bot
from googletrans import Translator
from pprint import pprint
from datetime import datetime
from handlers.users.text_handlers import menu2
from keyboards.default import instagram_menu, ob_havo_menu, uz_citys
import requests

translater =Translator()


def weather(city_name):
    parametres = {
        "q": city_name,
        "appid": "b01e7608c07f15c54ff9d9b64d478705",
        "units": "metric"
    }

    res = requests.get("https://api.openweathermap.org/data/2.5/weather", params=parametres).json()
    pprint(res)
    temp = res['main']['temp']
    temp_max = res["main"]["temp_max"]
    temp_min = res["main"]["temp_min"]
    city = res['name']
    description = res['weather'][0]['description']
    description = translate(description)
    wind_deg = check_deg(res["wind"]["deg"])
    wind = res['wind']['speed']
    sunrise = datetime.utcfromtimestamp(res['sys']['sunrise'] + res['timezone']).strftime("%Y.%d.%m  %H:%M:%S")
    sunset = datetime.utcfromtimestamp(res['sys']['sunset'] + res['timezone'])
    info = f"""🏙 {city} shaxrida
     Ob havo
 {description}
⛅️ Harorat {temp} °C
⛅️ Eng yuqorisi  {temp_max} °C
⛅️ Eng pasi {temp_min} °C

💨 shamol {wind_deg} dan esadi tezligi {wind} m/s  

☀️ quyosh chiqishi {sunrise}
🌇 quyosh botishi {sunset}

"""
    return info


def weather_from_location(latitude, longitude):
    parametres = {
        "lat": latitude,
        "lon": longitude,
        "appid": "b01e7608c07f15c54ff9d9b64d478705",
        "units": "metric"
    }

    res = requests.get("https://api.openweathermap.org/data/2.5/weather", params=parametres).json()
    pprint(res)
    temp = res['main']['temp']
    temp_max = res["main"]["temp_max"]
    temp_min = res["main"]["temp_min"]
    city = res['name']
    description = res['weather'][0]['description']
    description = translate(description)
    wind_deg = check_deg(res["wind"]["deg"])
    wind = res['wind']['speed']
    sunrise = datetime.utcfromtimestamp(res['sys']['sunrise'] + res['timezone']).strftime("%Y.%d.%m  %H:%M:%S")
    sunset = datetime.utcfromtimestamp(res['sys']['sunset'] + res['timezone'])
    info = f"""🏙 {city} shaxrida
         Ob havo
   {description}
⛅️ Harorat {temp} °C
⛅️ Eng yuqorisi  {temp_max} °C
⛅️ Eng pasi {temp_min} °C

💨 shamol {wind_deg} dan esadi tezligi {wind} m/s  

☀️ quyosh chiqishi {sunrise}
🌇 quyosh botishi {sunset}

    """
    return info


def check_deg(deg):
    dict_weather = {"Shimol (N)": 0, "Shimol-sharq (NNE)": 22.5, "Sharq (E)": 90, "Sharq-janub (ESE)": 112.5,
                    "Janub (S)": 180, "Janub-g’arb (SSW)": 202.5, "G’arb (W)": 270, "G’arb-shimol (WNW)": 292.5}
    for key, value in dict_weather.items():
        if value >= deg:
            return key


def translate(text):
    tr_text = translater.translate(text, dest="uz").text
    return tr_text


@bot.message_handler(func=lambda message: message.text == "Ob havo")
def ob_havo(message: Message):
    bot.send_message(message.chat.id, "Tugamlardan birini tanlang ", reply_markup=ob_havo_menu())
    bot.register_next_step_handler(message, get_weather_location_or_cit_name)


def get_weather_location_or_cit_name(message: Message):
    if message.text == "Menu":
        menu2(message)
    elif message.text:
        bot.send_message(message.chat.id, "Shaharni tanlang yoki kiriting!", reply_markup=uz_citys())
        bot.register_next_step_handler(message, get_weather)
    elif message.location:
        lat = message.location.latitude
        lon = message.location.longitude
        info_weather = weather_from_location(lat, lon)
        bot.send_message(message.chat.id, info_weather, reply_markup=ob_havo_menu())
        bot.register_next_step_handler(message, get_weather_location_or_cit_name)


def get_weather(message: Message):
    if message.text == "Menu":
        ob_havo(message)
    else:
        chat_id = message.chat.id
        info_weather = weather(message.text)
        bot.send_message(chat_id, info_weather, reply_markup=uz_citys())
        bot.register_next_step_handler(message, get_weather)
