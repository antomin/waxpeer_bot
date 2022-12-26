import telebot
from telebot import types

from common import generate_message
from settings import CHAT_ID, TG_TOKEN
from waxpeer_api import buy_item

bot = telebot.TeleBot(TG_TOKEN)


def send_notification(item, result=None):
    message = generate_message(item)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Buy', callback_data=f'buy__{item["id"]}__{item["price"]}'))

    bot.send_message(CHAT_ID, message, disable_web_page_preview=True, reply_markup=markup)

    if result:
        if result['success']:
            bot.send_message(CHAT_ID, 'Auto buy success!')
        else:
            bot.send_message(CHAT_ID, result['msg'])


@bot.callback_query_handler(lambda callback: callback.data and callback.data.startswith('buy__'))
def run_buy_func(callback: types.CallbackQuery):
    good_info = callback.data.split('__')
    good_id, good_price = good_info[1], good_info[2]

    result = buy_item(good_id, good_price)

    if result['success']:
        bot.answer_callback_query(callback_query_id=callback.id, text='Buy success!', show_alert=True)
    else:
        bot.answer_callback_query(callback_query_id=callback.id, text=result['msg'], show_alert=True)


if __name__ == "__main__":
    bot.infinity_polling()
