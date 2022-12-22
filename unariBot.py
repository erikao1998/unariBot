from dotenv import load_dotenv
import os
from telegram.ext import Updater
import logging
import telegram
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import requests

r = requests.get("https://kitchen.kanttiinit.fi/restaurants/")
data = r.json()

restaurants = [restaurant["name"] for restaurant in data]

def get_menu(id):
    r = requests.get(f"https://kitchen.kanttiinit.fi/restaurants/{id}/menu")
    restaurant = r.json()
    if restaurant["menus"]:
        courses = [menu["courses"] for menu in restaurant["menus"]]
        return [course["title"] for course in courses[0]]
    else:
        return 0


def search_restaurant(name):
    for restaurant in data:
        if restaurant["name"] == name:
            return get_menu(restaurant["id"])
    return 0

load_dotenv()
tg_token = os.getenv("TELEGRAM_TOKEN")
chatId = os.getenv("CHAT_ID")

bot = telegram.Bot(token=tg_token)

updater = Updater(token=tg_token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name) - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    restaurant_list = ' \n'.join(restaurants)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Moi, olen Unaribotti. Minulta saat opiskelijaravintoloiden ruokalistat tälle päivälle! Valitse joku näistä ravintoloista:")
    context.bot.send_message(chat_id=update.effective_chat.id, text=restaurant_list)


def menu(update: Update, context: CallbackContext):
    searched_menu = search_restaurant(context.args[0])
    message = ' \n'.join(searched_menu)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

menu_handler = CommandHandler('menu', menu)
dispatcher.add_handler(menu_handler)

updater.start_polling()
updater.idle()