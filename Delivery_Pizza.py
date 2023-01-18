from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import sqlite3
from constants import get_products_query, create_new_user

TOKEN = "5818277153:AAE9MmEDeUi_6krfN2je2mNINZ4woKHvnlg"

bot = TeleBot(token=TOKEN, parse_mode=None)


def main_menu_keyboard():
    '''
    This function create firstly menu in our telegram bot.
    :return: class Object ReplyKeyboardMarkup
    '''

    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    menu = KeyboardButton("Menu🍕")
    cart = KeyboardButton("Basket🧺")
    contacts = KeyboardButton('Contacts☎️')
    feedback = KeyboardButton('Feedback📝')
    delivery = KeyboardButton('Delivery🚚')
    settings = KeyboardButton('Settings⚙️')

    markup.add(menu)
    markup.add(cart, delivery)
    markup.add(contacts, feedback)
    markup.add(settings)

    return markup


def get_product_names() -> list:
    products = []

    try:
        conn = sqlite3.connect("Pizza_db")
        cursor = conn.cursor()
        sql = get_products_query()
        cursor.execute(sql)


        for product in cursor.fetchall():
            products.append(product[0])


    except Exception as e:

        print(e)

    return products


def get_user_details_k():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    get_phone_button = KeyboardButton("Write your phone number: ")
    get_address_button = KeyboardButton("Write your address")

    markup.add(get_phone_button)
    markup.add(get_address_button)

    return markup


def create_user(chat_id):

    try:
        conn = sqlite3.connect('Pizza_db')
        cursor = conn.cursor()
        sql = create_new_user(chat_id)
        cursor.execute(sql)


    except Exception as e:
        print(e)


@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    chat_id = message.chat.id
    create_user(chat_id)
    reply = f"Welcome <u>@{message.from_user.username}</u>💛 to our delivery_bot!"
    bot.reply_to(message, reply, parse_mode='html', reply_markup=get_user_details_k())

    print(f'Name_of_user - {message.from_user.first_name}')
    print(f'Username_of_user - @{message.from_user.username}')
    print(f'ID_user - {message.from_user.id}')



def menu_pizza_keyboard():
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
        if len(row) == 3:
            keyboard.add(*row)
            row = []

    if row:
        keyboard.add(*row)

    back_button = KeyboardButton("🔙")
    keyboard.add(back_button)

    return keyboard



@bot.message_handler(func=lambda message: message.text == 'Menu🍕')
def menu_handler(message):

    reply1 = 'Choose your favourite pizza:'
    bot.reply_to(message, reply1, reply_markup=menu_pizza_keyboard())



@bot.message_handler(content_types=['text'])
def message_handler(message):
    if message.text == 'Menu🍕':
        bot.reply_to(message, 'Choose your favourite pizza:🍕', reply_markup=menu_pizza_keyboard())

    if message.text == 'Contacts☎️':
        bot.reply_to(message, '- Telephone number: +998(93)549-13-33\n- Free Call✅', reply_markup=main_menu_keyboard())

    if message.text == 'Feedback📝':
        bot.reply_to(message, 'Delivery service control:\n'
                              'We thank you for your choice and will be glad,if you help improve the quality of our service!\n'
                              'Rate our work on a 5-point scale.', reply_markup=feedback_keyboard())

    if message.text == '🔙':
        bot.reply_to(message, f'Welcome <b>{message.from_user.first_name}💛</b>!\n'
                              f'What will you order?', parse_mode='html', reply_markup=main_menu_keyboard())

    if message.text == '😊 I liked everything, 5 ❤️':
        bot.reply_to(message,
                     'We are glad that you were satisfied. We will continue to try to please you and your loved ones🤗\n\nYour Iskra_Pizza ❤️',
                     reply_markup=main_menu_keyboard())

    if message.text == '☺️Normal, on 4 ⭐️⭐️⭐️⭐️':
        bot.reply_to(message, 'We are glad that you liked it 😊. What else can we do to improve our service?🤔',
                     reply_markup=back_keyboard())

    if message.text == 'Back⬅️':
        bot.reply_to(message, 'What will you order?🍔', reply_markup=main_menu_keyboard())

    if message.text == '😐 Satisfactory for 3 ⭐️⭐️⭐️':
        bot.reply_to(message, 'We are sorry that you were not satisfied with our service.\n'
                              'Help us become better, leave your comments and suggestions 👇🏻.\n'
                              'We will work to improve the service 🙏🏻', reply_markup=back_keyboard())


    if message.text == "☹️Didn't like it, 2 ⭐️⭐️":
        bot.reply_to(message, 'We are sorry that you were not satisfied with our service.\n'
                          'Help us become better, leave your comments and suggestions 👇🏻.\n'
                          'We will work to improve the service 🙏🏻', reply_markup=back_keyboard())

    if message.text == 'Settings⚙️':
        bot.reply_to(message, '-Settings-', reply_markup=back_keyboard())

    if message.text == 'Delivery🚚':
        bot.reply_to(message,
                 'If we do not have time🕘 to deliver the order within 60 minutes, we will send you a promotional code📱 for a large pizza as a gift!🎁\n\n'
                 '- Free delivery✅\n'
                 '- Order amount from 45.000 sum💴')

'''

def menu_pizza_keyboard():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    button1 = KeyboardButton('Peperoni🍕')
    button2 = KeyboardButton('Margarita🍕')
    button3 = KeyboardButton('Hawai🍕')
    button4 = KeyboardButton('Comby🍕')
    button5 = KeyboardButton('Carbonara🍕')
    button6 = KeyboardButton('4seasons🍕')
    button7 = KeyboardButton('🔙')

    markup.add(button1, button2, button3)
    markup.add(button4, button5, button6)
    markup.add(button7)

    return markup
'''

def feedback_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button1 = KeyboardButton('😊 I liked everything, 5 ❤️')
    button2 = KeyboardButton('☺️Normal, on 4 ⭐️⭐️⭐️⭐️')
    button3 = KeyboardButton('😐 Satisfactory for 3 ⭐️⭐️⭐️')
    button4 = KeyboardButton("☹️Didn't like it, 2 ⭐️⭐️")

    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)

    return markup



def back_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    button = KeyboardButton('Back⬅️')
    markup.add(button)

    return markup


bot.infinity_polling()

