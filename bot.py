import logging
import os

import dotenv
import rpyc as rpyc
import telebot
from deeppavlov import build_model

from states.AbstractState import BotContext
from states.ArgsDto import ArgsDto

dotenv.load_dotenv()
bot_token = os.environ.get("bot_token")

logging.basicConfig(level=logging.DEBUG)

intent_catcher_model = build_model('intent_catcher_config.json')
context_qa_model = build_model('contextQAConfig.json')

bot = telebot.TeleBot(bot_token)
intent_catcher = rpyc.connect("localhost", 18861)


@bot.message_handler()
def handle_message(message):
    context = BotContext(args=ArgsDto(intent_catcher=intent_catcher,
                                      context_qa=context_qa_model,
                                      message=message))
    bot.send_message(message.from_user.id, context.run())


try:
    logging.info("Started")
    bot.polling()
except Exception as e:
    print(e)
