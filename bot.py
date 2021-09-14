import os

import dotenv
import telebot
from deeppavlov import build_model
from deeppavlov.core.common.file import read_json

dotenv.load_dotenv()
bot_token = os.environ.get("bot_token")

bot = telebot.TeleBot(bot_token)

model_config = read_json('config.json')
model = build_model(model_config, download=True)
context = ''

@bot.message_handler(commands=['help', 'h'])
def handle_help(message):
    bot.send_message(message.from_user.id, "Need help?")


@bot.message_handler(commands=['context','c'])
def parse_context(message):
    context = message.text


@bot.message_handler(commands=['context','c'])
def answer_question(message):
    question:str = message.text
    answers = model([context],question)

@bot.message_handler()
def handle_message(message):
    bot.send_message(message.from_user.id, "Hello")


while True:
    try:
        bot.polling(none_stop=True)
    except e:
        print(e)
