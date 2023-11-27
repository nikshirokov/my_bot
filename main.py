import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from datetime import datetime

logging.basicConfig(filename='bot.log', level=logging.INFO)


today = datetime.now()
planet_dict = {'Mars': ephem.Mars(today), 'Venus': ephem.Venus(today), 'Saturn': ephem.Saturn(today), 'Jupiter': ephem.Jupiter(today),
               'Neptune': ephem.Neptune(today), 'Uranus': ephem.Uranus(today), 'Mercury': ephem.Mercury(today)}

def greet_user(update, context):
    logging.info('Вызван /start')
    update.message.reply_text('Здравствуй, пользователь!')

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
    text = update.message.text
    logging.info(f'Введен текст: {text}')
    update.message.reply_text(text)

def main():
    mybot = Updater(settings.API_KEY, use_context = True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))


    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()
