import telebot
from datetime import date, timedelta, datetime
import time
from pars import get_info, get_response, get_info2
from configu import TOKEN
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,

)


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome_message(message):
    text = """Здравствуйте! Это бот для просмотра погоды."""
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    continue_step = InlineKeyboardButton("Продолжить", callback_data="continue")
    markup.add(continue_step)
    bot.send_message(message.chat.id, text, reply_markup=markup)
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if current_time == '10:00':
            new_date = date.today()
            new_link = f'https://sinoptik.ua/погода-{city_name.lower()}/{str(new_date)}'
            new_html = get_response(new_link)
            weather_for_today = str(get_info(new_html))
            time.sleep(10)
            bot.send_message(message.chat.id, f"""Авторассылка погоды на сегодня - {weather_for_today}""")
            time.sleep(60)
        elif current_time == '22:00':
            today = date.today()
            tomorrow = today + timedelta(days=1)
            new_date = tomorrow
            new_link = f'https://sinoptik.ua/погода-{city_name.lower()}/{str(new_date)}'
            new_html = get_response(new_link)
            weather_for_tomorrow = str(get_info2(new_html))
            bot.send_message(message.chat.id, f"""Авторассылка погоды на завтра - {weather_for_tomorrow}""")
            time.sleep(60)


@bot.callback_query_handler(func=lambda call: call.data == "continue")
def choose_city(call):
    text = "Напишите название города:"
    bot.send_message(call.message.chat.id, text)
    bot.register_next_step_handler(message=call.message, callback=city_weather)


city_name = ""


def city_weather(message):
    global city_name
    city_name = message.text
    with open("users.txt", "a", encoding="utf-8") as file:
        user_name = message.from_user.username
        user_date = message.from_user
        full_text = f"""Время: {user_date}\nЛогин пользователя: {user_name}\nТекст пользователя: {city_name}"""
        file.write(full_text)
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    weather_today_markup = InlineKeyboardButton("Погода сегодня", callback_data="weather_today")
    weather_tomorrow_markup = InlineKeyboardButton("Погода завтра", callback_data="weather_tomorrow")
    other_city_markup = InlineKeyboardButton("Другой город", callback_data="other")
    markup.add(weather_today_markup, weather_tomorrow_markup, other_city_markup)
    text = """На какой день вас интересует погода?"""
    bot.send_message(message.chat.id, text, reply_markup=markup)

# other city
@bot.callback_query_handler(func=lambda call: call.data == 'other')
def choose_other_city(call):
    if call.data == 'other':
        choose_city(call=call)

@bot.callback_query_handler(func=lambda call: call.data == "weather_today")
def weather_today(call):
    new_date = date.today()
    new_link = f'https://sinoptik.ua/погода-{city_name.lower()}/{str(new_date)}'
    new_html = get_response(new_link)
    weather_for_today = str(get_info(new_html))
    bot.send_message(call.message.chat.id, f"""Погода на сегодня:\n{weather_for_today}""")


@bot.callback_query_handler(func=lambda call: call.data == "weather_tomorrow")
def weather_tomorrow(call):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    new_date = tomorrow
    new_link = f'https://sinoptik.ua/погода-{city_name.lower()}/{str(new_date)}'
    new_html = get_response(new_link)
    weather_for_tomorrow = str(get_info2(new_html))
    bot.send_message(call.message.chat.id, f"""Погода на завтра:\n{weather_for_tomorrow}""")


bot.infinity_polling()









