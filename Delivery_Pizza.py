from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3
from constants import get_products_query

TOKEN = "5818277153:AAE9MmEDeUi_6krfN2je2mNINZ4woKHvnlg"

bot = TeleBot(token=TOKEN, parse_mode=None)

def main_menu_keyboard():
    '''
    This function create firstly menu in our telegram bot.


    :return: class Object ReplyKeyboardMarkup
    '''
    cart = KeyboardButton("Basket")
    menu = KeyboardButton("Menu")

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(menu)
    keyboard.add(cart)

    return keyboard

def get_product_names() -> list:
    products = []

    try:
        conn = sqlite3.connect("Pizza_db")
        cursor = conn.cursor()
    except Exception as e:
        print(e)

@bot.message_handler(commands=['start'])
def start_handler(message):
    reply = f"Welcome {message.from_user.first_name}to our delivery_bot"
    bot.reply_to(message, reply, reply_markup=main_menu_keyboard())
    print(f'Username_of_user - {message.from_user.username}')

def menu_keyboard():
    '''
    This menu lights products in our database

    :return: class Object ReplyKeyboardMarkup
    '''

    products = get_product_names()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for product in products:
        button = KeyboardButton(product)
        row.append(button)
        if len(row) == 2:
            keyboard.add(*row)
            row = []

    if row:
        keyboard.add(*row)

    back_button = KeyboardButton("--Back--")

    keyboard.add(back_button)

    return keyboard

@bot.message_handler(func=lambda message: message.text == 'Menu')
def menu_handler(message):
    reply = 'Choose your favourite pizza:'
    bot.reply_to(message, reply, reply_markup=menu_keyboard)




bot.infinity_polling()