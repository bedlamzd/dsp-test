import requests
import shelve
import os

import telebot
import dotenv

from BotUser import BotUser

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)


def download_file(file_id):
    file_info = bot.get_file(file_id)
    return requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')


# def save_file(path, file):
#     path = pathlib.Path(path)
#     path.parent.mkdir(parents=True, exist_ok=True)
#     with open(path, 'wb') as f:
#         f.write(file)
#     print('File saved')


@bot.message_handler(commands=['start'])
def welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'This is test task for dsp Junior Developer')
    if (user_id := str(message.from_user.id)) not in db:
        db.update({user_id: BotUser(user_id)})


@bot.message_handler(commands='users')
def get_known_users(message: telebot.types.Message):
    text = '\n'.join(user_id for user_id in db)
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['voice'])
def process_voice(message: telebot.types.Message):
    if user := db.get(str(message.from_user.id)):
        voice = download_file(message.voice.file_id).content
        user.add_voice(voice)
        db.update({user.id: user})
        bot.reply_to(message, 'Audio saved.')
    else:
        bot.send_message(message.chat.id, 'Unknown user. Send /start first.')


if __name__ == '__main__':
    db = shelve.open('bot_db')
    try:
        bot.polling()
    except KeyboardInterrupt:
        print('Keyboard interruption occurred.')
    finally:
        db.close()
