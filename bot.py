import dotenv
import logging
import os
import telebot
from deeppavlov import build_model
from deeppavlov.core.common.file import read_json

dotenv.load_dotenv()
bot_token = os.environ.get("bot_token")

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(bot_token)
model_config = read_json('config.json')
model = build_model(model_config, download=True)
context: str = ""


@bot.message_handler(commands=['help', 'h'])
def handle_help(message):
    bot.send_message(message.from_user.id, "Need help?")


@bot.message_handler(commands=['c'])
def parse_context(message):
    global context
    context = message.text[3:]
    bot.send_message(message.from_user.id, "Accepted")


@bot.message_handler(commands=['q'])
def answer_question(message):
    question: str = message.text
    logging.debug(context)
    answers = model([context], [question])
    logging.info(answers)
    bot.send_message(message.from_user.id, answers)


@bot.message_handler()
def handle_message(message):
    bot.send_message(message.from_user.id, "Hello")


while True:
    try:
        logging.debug("Started")
        logging.info(model(['DeepPavlov is library for NLP and dialog systems.'], ['What is DeepPavlov?']))
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
