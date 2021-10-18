import logging
import os

import dotenv
import telebot
import wikipedia as wiki
from deeppavlov import build_model
from deeppavlov.core.common.file import read_json

dotenv.load_dotenv()
bot_token = os.environ.get("bot_token")

wiki.set_lang('ru')

logging.basicConfig(level=logging.DEBUG)

bot = telebot.TeleBot(bot_token)
model_config = read_json('config.json')
model = build_model(model_config, download=True)

CONTEXT = {}
RESULTS = {}


def get_context(user_id) -> str:
    try:
        return CONTEXT[user_id]
    except KeyError:
        CONTEXT[user_id] = ''
        return CONTEXT[user_id]


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.from_user.id,
                     """Этот бот предназначен для демонстрации работы вопросно-ответной системы на основе модели BERT.
Команды:
/c контекст - задать текст, в котором будет производиться поиск ответов на вопросы.
/q вопрос - задать вопрос по тексту
/wiki - искать статью в Википедии
/start - сбросить контекст и начать заново
/help - вывести это сообщение""")


@bot.message_handler(commands=['c'])
def parse_context(message):
    CONTEXT[message.from_user.id] = message.text[3:]
    bot.send_message(message.from_user.id, "Принято")


@bot.message_handler(commands=['q'])
def answer_question(message):
    if len(get_context(message.from_user.id)) > 0:
        question: str = message.text[1:]
        logging.debug(get_context(message.from_user.id))
        answers = model(get_context(message.from_user.id).split(". "), [question])
        logging.info(answers)
        bot.send_message(message.from_user.id, answers)
    else:
        bot.send_message(message.from_user.id, "Контекст не задан")


@bot.message_handler(commands=['start'])
def start(message):
    CONTEXT[message.from_user.id] = ''
    bot.send_message(message.from_user.id, "Контекст сброшен")


@bot.message_handler(commands=['wiki'])
def wiki_search(message):
    if len(message.text[5:]) > 0:
        results = wiki.search(message.text[5:])
        RESULTS[message.from_user.id] = results
        answer_message = ''
        for i, result in zip(range(len(results)), results):
            answer_message += f"/{i} {result}\n"
        bot.send_message(message.from_user.id, answer_message)
    else:
        bot.send_message(message.from_user.id, "Введите поисковый запрос после /wiki")


@bot.message_handler(regexp='/[0-9]')
def handle_article(message):
    try:
        articles = RESULTS[message.from_user.id]
    except KeyError:
        bot.send_message(message.from_user.id, "Сначала введите /wiki для поиска статьи")
        return
    article_title = articles[int(message.text[1:2])]
    page = wiki.page(article_title)
    CONTEXT[message.from_user.id] = page.content
    RESULTS[message.from_user.id] = None
    bot.send_message(message.from_user.id, f"Выбрана статья {page.title} {page.url}")


@bot.message_handler()
def handle_message(message):
    bot.send_message(message.from_user.id, "Не понятное сообщение, нажмите /help что бы узнать как пользоваться ботом")


try:
    logging.info("Started")
    bot.polling()
except Exception as e:
    print(e)
