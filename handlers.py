from selenium.webdriver.common.by import By

from common import RARITY_DICT, print_time, read_cache, write_to_cache
from settings import (FLOAT_AUTOBUY_TERMS, FLOAT_NOTIFICATION_TERMS,
                      REPEAT_MSG, STICKER_SEARCH_STRING,
                      STICKERS_AUTOBUY_TERMS)
from telegram import send_notification
from waxpeer_api import buy


def parse_item(item):
    item_url = item.find_element(By.XPATH, './div[@class="item_body"]/a').get_attribute('href')
    item_id = item_url.split('/')[-1]
    if not REPEAT_MSG and item_id in read_cache():
        return
    stickers_info = get_stickers(item)
    if stickers_info == 'search_not_found':
        return
    price = item.find_element(By.XPATH, './/div[@class="prices f"]//span[@class="c-usd"]').text
    steam_price = item.find_element(By.XPATH, './/div[@class="item_top f ft gray"]//span[@class="c-usd"]').text
    name_model = item.find_element(By.XPATH, './/a[@class="name ovh"]').text
    name_gray = item.find_element(By.XPATH, './/div[@class="gray"]').text
    rarity = item.find_element(By.XPATH, './/div[@class="thumb_bg"]').get_attribute('style')
    try:
        item_float = item.find_element(By.XPATH, './/p[@class="num"]').text
    except:
        item_float = None

    item_content = {
        'id': item_url.split('/')[-1],
        'url': item_url,
        'price': float(price.replace(' ', '')),
        'steam_price': float(steam_price.replace(' ', '')),
        'title': name_model.replace('\n', ' ') + ' (' + name_gray + ')',
        'item_float': float(item_float) if item_float else None,
        'stickers': stickers_info[0],
        'stickers_sum_price': stickers_info[1],
        'rarity': RARITY_DICT.get(rarity)
    }

    item_handler(item_content)
    write_to_cache(item_content['id'])


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
