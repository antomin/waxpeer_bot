import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
