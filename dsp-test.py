import telebot
import requests
import json

from audio_magick import save_voice_to_wav

data_list = []

bot_data = json.load(open('bot.json'))
TOKEN = bot_data['TOKEN']

bot = telebot.TeleBot(TOKEN)


class Bot_user:
    def __init__(self, id):
        self.id = id
        self.records = []
        self.record_id = 0

    def add_voice(self, voice):
        voice_name = f'audio_message_{self.record_id}.wav'
        self.record_id += 1
        save_voice_to_wav(fr'.\{self.id}\{voice_name}', voice)
        self.records.append(voice_name)

    def add_image(self, image):
        pass


known_users = dict()


def download_file(file_id):
    file_info = bot.get_file(file_id)
    return requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')


def save_file(path, file):
    with open(path, 'wb') as f:
        f.write(file)
    print('File saved')


@bot.message_handler(commands=['start'])
def welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'This is test task for dsp Junior Developer')
    if (user_id := message.from_user.id) not in known_users:
        user = Bot_user(user_id)
        known_users[user_id] = user


@bot.message_handler(commands='users')
def get_known_users(message: telebot.types.Message):
    text = '\n'.join(f'{user_id}' for user_id in known_users)
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['voice'])
def process_voice(message: telebot.types.Message):
    try:
        user = known_users[message.from_user.id]
        voice = download_file(message.voice.file_id).content
        user.add_voice(voice)
        bot.reply_to(message, 'Audio saved')
    except KeyError:
        bot.send_message(message.from_user.id, 'Unknown user. Send /start first.')


bot.polling()
