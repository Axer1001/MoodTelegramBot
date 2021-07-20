import telebot
from telebot import types
from db import Database, User
import tracks

TOKEN = 'YOUR_TOKEN_HERE'
users = Database()
bot = telebot.TeleBot(TOKEN)

currentUser = User('')
moods = {
    'Грустное': 'sad',
    'Весёлое': 'fun',
    'Спокойное': 'calm',
    'Энергичное': 'active',
    'Любое': 'all'
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "Привет! Чтобы начать работу, отправь мне свой токен от Яндекс.Музыки")
    bot.register_next_step_handler(message, get_token)


def get_token(message):
    currentUser.yandexToken = message.text
    bot.delete_message(message.chat.id, message.message_id)
    users.add_user(str(message.from_user.id), currentUser.yandexToken)

    markup = types.ReplyKeyboardMarkup()
    markup.row('Весёлое')
    markup.row('Грустное')
    markup.row('Энергичное')
    markup.row('Спокойное')
    markup.row('Любое')
    bot.send_message(message.chat.id, "Данные сохранены, теперь выбери настроение для плейлиста!",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_playlist(message):
    if message.text not in moods.keys():
        return

    bot.send_message(message.chat.id, 'Генерирую плейлист!')
    track_list = tracks.get_tracks(users.get_user_data(
        str(message.from_user.id)).yandexToken, moods[message.text])
    print(track_list)
    for trck in track_list:
        trck = open(trck, 'rb')
        bot.send_audio(message.chat.id, trck)
    bot.send_message(
        message.chat.id, 'Если хочешь еще один плейлист, просто выбери настроение :)')


bot.polling()
