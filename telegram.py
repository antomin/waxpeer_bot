import telebot
from telebot import types

from settings import CHAT_ID, TG_TOKEN
from common import generate_message
from waxpeer_api import buy_item

bot = telebot.TeleBot(TG_TOKEN)


def send_notification(item):
    message = generate_message(item)
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Buy', callback_data=f'buy_{item["id"]}'),
    )
    bot.send_message(CHAT_ID, message, disable_web_page_preview=True, reply_markup=markup)


def send_autobuy_notification(item):
    message = generate_message(item)
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Open', url=item['url']),
    )
    bot.send_message(CHAT_ID, 'ПРОДАЖА!!!\n' + message, disable_web_page_preview=True, reply_markup=markup)
