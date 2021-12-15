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


class IntentCatcher:
    def __init__(self):
        self.intent_catcher = rpyc.connect("localhost", 18861)

    def __call__(self, message):
        intent = self.intent_catcher.root.get_intent(message)
        logging.debug("Message: " + message)
        logging.debug("Intent: " + intent)
        return intent


get_intent = IntentCatcher()

context_qa_model = build_model('contextQAConfig.json')


@bot.message_handler(content_types=['location'])
@bot.message_handler()
def handle_message(message: telebot.types.Message):
    logging.debug("message handler activated")
    if message.content_type != "location":
        intent = get_intent(message.text)
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
