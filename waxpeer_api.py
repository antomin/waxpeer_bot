import json

import requests

from settings import STEAM_PARTNER, STEAM_TOKEN, WAXPEER_API_KEY

HEADERS = {'accept': 'application/json'}


def buy_item(good_id, good_price):
    good_price = float(good_price) * 1000
    url = f'https://api.waxpeer.com/v1/buy-one-p2p?api={WAXPEER_API_KEY}&item_id={good_id}&token={STEAM_TOKEN}&price={good_price}&partner={STEAM_PARTNER}'

    response = requests.get(url=url, headers=HEADERS)

    return json.loads(response.text)


def auto_bay_item(item):
    good_price = item['price'] * 1000
    good_id = item['id']
    url = f'https://api.waxpeer.com/v1/buy-one-p2p?api={WAXPEER_API_KEY}&item_id={good_id}&token={STEAM_TOKEN}&price={good_price}&partner={STEAM_PARTNER}'

    response = requests.get(url=url, headers=HEADERS)

    return json.loads(response.text)
