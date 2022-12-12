import os
import time

import undetected_chromedriver

from settings import BASE_DIR, HEADLESS

RARITY_DICT = {
    'color: rgb(176, 195, 217);': 'Consumer Grade',
    'color: rgb(94, 152, 217);': 'Industrial Grade',
    'color: rgb(75, 105, 255);': 'Mil-Spec Grade',
    'color: rgb(136, 71, 255);': 'Restricted',
    'color: rgb(211, 44, 230);': 'Classified',
    'color: rgb(235, 75, 75);': 'Covert'
}


def write_to_cache(item_id):
    with open(f'{BASE_DIR}/cache.txt', 'a', encoding='utf-8') as file:
        file.write(item_id + '\n')


def read_cache():
    with open(f'{BASE_DIR}/cache.txt', 'r', encoding='utf-8') as file:
        ids_list = file.read().splitlines()
    return ids_list


def get_driver():
    options = undetected_chromedriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.headless = HEADLESS
    return undetected_chromedriver.Chrome(options=options)


def print_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        print(f'{func.__name__}: {time.time() - start_time}c.')
        return res
    return wrapper
