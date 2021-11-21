import logging
import os

import dotenv
import telebot

from states.AbstractState import BotContext

dotenv.load_dotenv()
bot_token = os.environ.get("bot_token")

logging.basicConfig(level=logging.DEBUG)

bot = telebot.TeleBot(bot_token)


@bot.message_handler()
def handle_message(message):
    context = BotContext(message=message)
    bot.send_message(message.from_user.id, context.run())


try:
    logging.info("Started")
    bot.polling()
except Exception as e:
    print(e)
