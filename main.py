import telebot
from telebot import types

TOKEN = '1864103746:AAGy24BcsZRNZ0RsIwzp41fiZ4dl4w85tgI'
username = ''
password = ''

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Весёлое')
    markup.row('Любое')
    markup.row('Энергичное')
    markup.row('Грустное')
    bot.reply_to(message, "Привет, выбери настроение и я составлю тебе плейлист!", reply_markup=markup)

@bot.message_handler(content_types=['text'] )
def send_audio(message):
    bot.reply_to(message, )


bot.polling()