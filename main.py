import os
import shelve
import logging

import dotenv

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler

from BotUser import BotUser
from image_magick import read_img_from_bytearray, contains_face

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dotenv.load_dotenv()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat.id, text='This is test task for dsp Junior Developer')
    if (user_id := str(update.message.from_user.id)) not in db:
        db.update({user_id: BotUser(user_id)})


def help(update: Update, context: CallbackContext):
    help_message = 'Send voice and I will save it as .wav file.\n'
    help_message += 'Send your photo and I will tell if it has faces.\n'
    help_message += 'Source: https://github.com/bedlamzd/dsp-test'
    context.bot.send_message(update.message.chat.id, text=help_message)


def process_voice(update: Update, context: CallbackContext):
    if user := db.get(str(update.message.from_user.id)):
        voice = update.message.voice.get_file().download_as_bytearray()
        user.add_voice(voice)
        db.update({user.id: user})
        context.bot.send_message(update.message.chat.id, reply_to_message_id=update.message.message_id,
                                 text='Converting...')
        context.bot.send_document(update.message.chat.id, user.get_audio(user.record_id - 1))
    else:
        context.bot.send_message(update.message.chat.id, 'Unknown user. Send /start first.')


def process_img(update: Update, context: CallbackContext):
    if user := db.get(str(update.message.from_user.id)):
        img = sorted(update.message.photo, key=lambda img: img.file_size, reverse=True)[0]
        context.bot.send_message(update.message.chat.id, text=f'Processing {img.file_id} img...')
        img = read_img_from_bytearray(img.get_file().download_as_bytearray())
        if contains_face(img):
            context.bot.send_message(update.message.chat.id, text=f'Img contains face!')
            user.add_image(img)
        else:
            context.bot.send_message(update.message.chat.id, text=f'Img does not contain face...')
        db.update({user.id: user})
    else:
        context.bot.send_message(update.message.chat.id, 'Unknown user. Send /start first.')


if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    URL = os.environ.get('URL')
    PORT = os.environ.get('PORT')

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    voice_handler = MessageHandler(Filters.voice, process_voice)
    photo_handler = MessageHandler(Filters.photo, process_img)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(voice_handler)
    dispatcher.add_handler(photo_handler)

    db = shelve.open('bot_db')
    updater.start_webhook(
        listen='0.0.0.0',
        port=PORT,
        url_path=TOKEN
    )
    updater.bot.set_webhook(URL + TOKEN)
