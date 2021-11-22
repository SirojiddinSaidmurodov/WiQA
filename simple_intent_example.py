import logging
import os

import dotenv
import telebot
from deeppavlov import build_model

dotenv.load_dotenv()
bot_token = os.environ.get("bot_token")

logging.basicConfig(level=logging.DEBUG)

intent_catcher_model = build_model('intent_catcher_config.json')

bot = telebot.TeleBot(bot_token)


@bot.message_handler()
def handle_message(message):
    bot.send_message(message.from_user.id, intent_catcher_model([message.text, ])[0])


if __name__ == '__main__':

    try:
        logging.info("Started")
        bot.polling()
    except Exception as e:
        print(e)
