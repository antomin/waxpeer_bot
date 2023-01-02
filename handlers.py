from selenium.webdriver.common.by import By

from common import RARITY_DICT, read_cache, write_to_cache
from settings import (CACHE_ENABLE, FLOAT_AUTOBUY_TERMS,
                      FLOAT_NOTIFICATION_TERMS, GLOVES_COVERT_LIST,
                      KNIFE_COVERT_LIST, MIN_STICKERS_SUM, NAME_EXCEPTIONS,
                      STICKER_SEARCH_STRING, STICKERS_AUTOBUY_TERMS)
from telegram import send_notification
from waxpeer_api import auto_bay_item


def parse_item(item):
    try:
        item_url = item.find_element(By.XPATH, './div[@class="item_body"]/a').get_attribute('href')
    except:
        item_url = 'https://waxpeer.com'

    item_id = item_url.split('/')[-1]

    if CACHE_ENABLE and item_id in read_cache():
        return

    try:
        name_model = item.find_element(By.XPATH, './/a[@class="name ovh"]').text
    except:
        name_model = ''

    stickers_info = get_stickers(item)
    if stickers_info == 'search_not_found':
        return

    try:
        price = item.find_element(By.XPATH, './/div[@class="prices f"]//span[@class="c-usd"]').text
    except:
        return

    try:
        steam_price = item.find_element(By.XPATH, './/div[@class="item_top f ft gray"]//span[@class="c-usd"]').text
    except:
        return

    try:
        name_gray = item.find_element(By.XPATH, './/div[@class="gray"]').text
    except:
        name_gray = ''

    try:
        rarity = item.find_element(By.XPATH, './/div[@class="thumb_bg"]').get_attribute('style')
    except:
        rarity = ''

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

    for string in NAME_EXCEPTIONS:
        if string in item_content['title']:
            return

    item_handler(item_content)

    if CACHE_ENABLE:
        write_to_cache(item_content['id'])


def get_stickers(item):
    stickers = []
    sum_price = 0

    try:
        sticker_list = item.find_elements(By.XPATH, './/li[@class="stickers_item ttip"]/div')

        for sticker in sticker_list:
            sticker_info = sticker.find_elements(By.XPATH, './p')
            sticker_name = sticker_info[0].get_attribute('innerHTML')
            if STICKER_SEARCH_STRING and STICKER_SEARCH_STRING not in sticker_name:
                stickers.append(None)
                continue
            try:
                sticker_price = float(
                    sticker.find_element(By.XPATH, './/span[@class="c-usd"]').get_attribute('innerHTML'))
            except:
                sticker_price = 0
            try:
                sticker_wear = sticker_info[1].find_elements(By.TAG_NAME, 'span')
                sticker_wear_value = sticker_wear[1].get_attribute('innerHTML')
            except:
                sticker_wear_value = None
            stickers.append({'name': sticker_name, 'wear': sticker_wear_value, 'price': sticker_price})
            sum_price += sticker_price if sticker_price else 0

        if STICKER_SEARCH_STRING and all(i is None for i in stickers):
            return 'search_not_found'
    except:
        return None

    return stickers, round(sum_price, 2)


def item_handler(item):
    if item['stickers']:
        # AUTO BUY BY STICKERS SUM PRICE
        for item_price, item_stickers_sum in STICKERS_AUTOBUY_TERMS.items():
            if item['price'] <= item_price and item['stickers_sum_price'] >= item_stickers_sum and \
                    item['price'] <= item['steam_price'] * 2:
                result = auto_bay_item(item)
                send_notification(item=item, result=result)
                return

        # NOTIFICATION BY STICKERS SUM
        if item['stickers_sum_price'] >= MIN_STICKERS_SUM:
            send_notification(item)

    if item['item_float'] and item['rarity']:
        # AUTO BUY BY FLOAT
        if item['item_float'] <= FLOAT_AUTOBUY_TERMS[item['rarity']][0] and \
                item['price'] <= item['steam_price'] * (1 + (FLOAT_AUTOBUY_TERMS[item['rarity']][1] / 100)) and \
                item['price'] <= item['steam_price'] * 2:
            result = auto_bay_item(item)
            send_notification(item=item, result=result)
            return

        # COVERT
        if item['rarity'] == 'Covert':
            # KNIFES
            for item_name in KNIFE_COVERT_LIST['items']:
                if item_name in item['title'] and item['item_float'] <= KNIFE_COVERT_LIST['range']:
                    send_notification(item)
                    return
            # GLOVES
            for item_name in GLOVES_COVERT_LIST['items']:
                if item_name in item['title']:
                    for float_range in GLOVES_COVERT_LIST['ranges']:
                        if float_range[0] <= item['item_float'] <= float_range[1]:
                            send_notification(item)
                            return
