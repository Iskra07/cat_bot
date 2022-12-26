import io

import telebot
from telebot.types import ReplyKeyboardMarkup,KeyboardButton
import requests

TOKEN = "5956193209:AAH55_tv76AItp2r5tqpdDipuGNdRSxhiRc"

bot = telebot.TeleBot(token=TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def welcome_message(message):
    welcome_message = 'Привет. Это бот достает фотки кошек из интернета!'

    bot.reply_to(message, welcome_message, reply_markup = keyboard())

@bot.message_handler(content_types=['text'])
def message_handle(message):
    if message.text == "Дай Кота!":
        cat = get_cat()
        bot.send_photo(message.chat.id, cat)
        bot.send_document(message.chat.id,cat)



def keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    button = KeyboardButton("Дай Кота!")
    keyboard.add(button)

    return keyboard

def get_cat():

    headers = {"content-type" : "application/jpeg"}
    reply = requests.get("https://api.api-ninjas.com/v1/randomimage?category=nature", headers = headers)
    image = reply.content
    image = io.BytesIO(image)

    return image


bot.infinity_polling()