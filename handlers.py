from selenium.webdriver.common.by import By
from settings import STICKERS_AUTOBUY_TERMS, FLOAT_AUTOBUY_TERMS, FLOAT_NOTIFICATION_TERMS, STICKER_SEARCH_STRING
from telegram import send_to_channel
from waxpeer_api import buy


def parse_item(html):



def get_stickers(item):
    stickers = []
    sum_price = 0
    try:
        sticker_list = item.find_elements(By.XPATH, './/li[@class="stickers_item ttip"]/div')
    except:
        return None
    for sticker in sticker_list:
        sticker_info = sticker.find_elements(By.XPATH, './p')
        sticker_name = sticker_info[0].get_attribute('innerHTML')
        if STICKER_SEARCH_STRING and STICKER_SEARCH_STRING not in sticker_name:
            stickers.append(None)
            continue
        try:
            sticker_price = float(sticker.find_element(By.XPATH, './/span[@class="c-usd"]').get_attribute('innerHTML'))
        except:
            sticker_price = None
        try:
            sticker_wear = sticker_info[1].find_elements(By.TAG_NAME, 'span')
            sticker_wear_value = sticker_wear[1].get_attribute('innerHTML')
        except:
            sticker_wear_value = None
        stickers.append({'name': sticker_name, 'wear': sticker_wear_value, 'price': sticker_price})
        sum_price += sticker_price if sticker_price else 0
    if STICKER_SEARCH_STRING and all(i is None for i in stickers):
        return 'search_not_found'
    return stickers, round(sum_price, 2)


def item_handler(item):
    msg_to_send = f'Name: {item["title"]}\n' \
                  f'Link: {item["url"]}\n' \
                  f'Float: {item["item_float"]}\n' \
                  f'Price: {item["price"]}\n' \
                  f'Steam price: {item["steam_price"]}\n\n'

    if item['stickers']:
        stickers_str = '\n\n'.join([f'{i["name"]}\nWear:{i["wear"]}\nPrice: {i["price"]}' for i in item['stickers']])
        msg_to_send += f'{stickers_str}\n\n' \
                       f'Total price: {item["stickers_sum_price"]}'

        # AUTO BUY BY STICKERS SUM PRICE
        for item_price, item_stickers_sum in STICKERS_AUTOBUY_TERMS.items():
            if item['price'] >= item_price and item['stickers_sum_price'] >= item_stickers_sum:
                send_to_channel(msg_to_send)
                buy(item)
                return

    # AUTO BUY BY FLOAT
    if item['item_float'] and item['item_float'] <= FLOAT_AUTOBUY_TERMS[item['rarity']][0] and \
            item['price'] <= item['steam_price'] * (1 + (FLOAT_AUTOBUY_TERMS[item['rarity']][1] / 100)):
        buy(item)
        return

    # NOTIFICATION BY FLOAT
    if item['item_float'] and item['item_float'] <= FLOAT_NOTIFICATION_TERMS[item['rarity']]:
        send_to_channel(msg_to_send)
