import logging
import os

import dotenv
import telebot
from deeppavlov import build_model
from deeppavlov.core.common.file import read_json

dotenv.load_dotenv()
bot_token = os.environ.get("bot_token")

logging.basicConfig(level=logging.DEBUG)

bot = telebot.TeleBot(bot_token)
model_config = read_json('config.json')
model = build_model(model_config, download=True)
context: str = ""


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.from_user.id,
                     """Этот бот предназначен для демонстрации работы вопросно-ответной системы на основе модели BERT. Команды:
/c контекст - задать текст, в котором будет производиться поиск ответов на вопросы.
/q вопрос - задать вопрос по тексту
/start - сбросить контекст и начать заново
/help - вывести это сообщение""")


@bot.message_handler(commands=['c'])
def parse_context(message):
    global context
    context = message.text[3:]
    bot.send_message(message.from_user.id, "Принято")


@bot.message_handler(commands=['q'])
def answer_question(message):
    if len(context) > 0:
        question: str = message.text[1:]
        logging.debug(context)
        answers = model([context], [question])
        logging.info(answers)
        bot.send_message(message.from_user.id, answers)
    else:
        bot.send_message(message.from_user.id, "Контекст не задан")


@bot.message_handler(commands=['start'])
def start(message):
    global context
    context = ''
    bot.send_message(message.from_user.id, "Контекст сброшен")


@bot.message_handler()
def handle_message(message):
    bot.send_message(message.from_user.id, "Не понятное сообщение, нажмите /help что бы узнать как пользоваться ботом")


while True:
    try:
        logging.info("Started")
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
