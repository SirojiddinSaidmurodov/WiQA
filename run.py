import logging
import os

import dotenv
import rpyc as rpyc
import telebot
from deeppavlov import build_model

from states.context import Bot

dotenv.load_dotenv()
bot_token = os.environ.get("bot_token")

logging.basicConfig(level=logging.DEBUG)

bot = telebot.TeleBot(bot_token)

context_qa_model = build_model('contextQAConfig.json')
intent_catcher = rpyc.connect("localhost", 18861)


@bot.message_handler(content_types=['location', 'text'])
def handle_message(message: telebot.types.Message):
    logging.debug("message handler activated")
    if message.content_type != "location":
        logging.debug("text received: " + message.text)
        intent: str = intent_catcher.root.get_intent(message.text)
        logging.debug("Intent: " + intent)
    else:
        intent = "greeting"
    context = Bot(message, intent)
    bot.send_message(message.from_user.id, context.run())


if __name__ == '__main__':
    try:
        logging.info("Started")
        bot.polling()
    except Exception as e:
        print(e)
