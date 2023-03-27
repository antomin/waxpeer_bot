import time

import undetected_chromedriver

from settings import BASE_DIR, HEADLESS

RARITY_DICT = {
    'color: rgb(176, 195, 217);': 'Consumer Grade',
    'color: rgb(94, 152, 217);': 'Industrial Grade',
    'color: rgb(75, 105, 255);': 'Mil-Spec Grade',
    'color: rgb(136, 71, 255);': 'Restricted',
    'color: rgb(211, 44, 230);': 'Classified',
    'color: rgb(235, 75, 75);': 'Covert',

}


def print_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        print(f'{func.__name__}: {time.time() - start_time}c.')
        return res
    return wrapper


def write_to_cache(item_id):
    with open(f'{BASE_DIR}/cache.txt', 'a', encoding='utf-8') as file:
        file.write(item_id + '\n')


def read_cache():
    with open(f'{BASE_DIR}/cache.txt', 'r', encoding='utf-8') as file:
        ids_list = file.read().splitlines()
    return ids_list


def get_driver():
    options = undetected_chromedriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--lang=en-US')
    options.headless = HEADLESS
    return undetected_chromedriver.Chrome(options=options, driver_executable_path=f'{BASE_DIR}/chromedriver')


def generate_message(item):
    message = f'Name: {item["title"]}\n' \
              f'Link: {item["url"]}\n' \
              f'Float: {item["item_float"]}\n' \
              f'Price: {item["price"]}\n' \
              f'Steam price: {item["steam_price"]}\n\n'
    if item['stickers']:
        stickers_str = '\n\n'.join([f'{i["name"]}\nWear:{i["wear"]}\nPrice: {i["price"]}' for i in item['stickers']])
        message += f'{stickers_str}\n\n' \
                   f'Total price: {item["stickers_sum_price"]}'

    return message
