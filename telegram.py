import requests
# import telebot

from settings import CHAT_ID, TG_TOKEN


def send_to_channel(message):
    requests.get(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}')


# bot = telebot.TeleBot(TG_TOKEN)
#
# def send_notification(item):
#     msg_to_send = f'Name: {item["title"]}\n' \
#                   f'Link: {item["url"]}\n' \
#                   f'Float: {item["item_float"]}\n' \
#                   f'Price: {item["price"]}\n' \
#                   f'Steam price: {item["steam_price"]}\n\n'
#     bot.send_message(CHAT_ID, message)
