from glob import glob
from random import choice
import ephem
from datetime import datetime
from utils import play_random_numbers,get_smile,main_keyboard
import logging

def greet_user(update, context):
    logging.info('Вызван /start')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!",
                              reply_markup= main_keyboard())

today = datetime.now()
planet_dict = {'Mars': ephem.Mars(today), 'Venus': ephem.Venus(today), 'Saturn': ephem.Saturn(today), 'Jupiter': ephem.Jupiter(today),
               'Neptune': ephem.Neptune(today), 'Uranus': ephem.Uranus(today), 'Mercury': ephem.Mercury(today)}


def planet_user(update, context):
    logging.info('Вызван /planet')
    planet_name = update.message.text.split()[1]
    logging.info(f'Введена планета {planet_name}')
    planet = planet_dict.get(planet_name)
    if planet != None:
        constellation = ephem.constellation(planet_dict[planet_name])
        update.message.reply_text(constellation[1])
    else:
        update.message.reply_text('Планета не найдена!')

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    logging.info(f'Введен текст: {text}')
    update.message.reply_text(f"{text} {context.user_data['emoji']}")

def guess_number(update, context):
    logging.info('Вызван /guess')
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"
    update.message.reply_text(message)

def send_picture(update, context):
    logging.info('Вызван /pictures')
    photos_list = glob('images/*.jp*g')
    pic_filename = choice(photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(pic_filename, 'rb'))

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard())