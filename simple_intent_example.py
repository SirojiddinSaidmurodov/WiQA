import logging
import os

import dotenv
import rpyc as rpyc
import telebot

dotenv.load_dotenv()
bot_token = os.environ.get("bot_token")

logging.basicConfig(level=logging.DEBUG)

intent_catcher = rpyc.connect("localhost", 18861)

bot = telebot.TeleBot(bot_token)


@bot.message_handler()
def handle_message(message):
    bot.send_message(message.from_user.id, intent_catcher.root.get_intent(message.text))


if __name__ == '__main__':
    try:
        logging.info("Started")
        bot.polling()
    except Exception as e:
        print(e)
