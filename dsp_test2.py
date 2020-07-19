import os
import shelve
import logging

import dotenv

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler

from BotUser import BotUser

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dotenv.load_dotenv()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat.id, text='This is test task for dsp Junior Developer')
    if (user_id := str(update.message.from_user.id)) not in db:
        db.update({user_id: BotUser(user_id)})


def process_voice(update: Update, context: CallbackContext):
    if user := db.get(str(update.message.from_user.id)):
        voice = update.message.voice.get_file.download()
        user.add_voice(voice)
        db.update({user.id: user})
        context.bot.send_message(update.message.chat.id, reply_to_message_id=update.message.message_id,
                                 text='Audio saved.')
    else:
        context.bot.send_message(update.message.chat.id, 'Unknown user. Send /start first.')


if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    URL = os.environ.get('URL')
    PORT = os.environ.get('PORT')

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    voice_handler = MessageHandler(Filters.voice, process_voice)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(voice_handler)

    db = shelve.open('bot_db')
    try:
        updater.start_webhook(
            listen='0.0.0.0',
            port=PORT,
            url_path=TOKEN
        )
        updater.bot.set_webhook(URL + TOKEN)
    finally:
        db.close()
