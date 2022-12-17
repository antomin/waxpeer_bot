import requests

from settings import WAXPEER_API_KEY, STEAM_TOKEN, STEAM_PARTNER

HEADERS = {'accept': 'application/json'}


def buy_item(item):
    item_id = item['id']
    item_price = item['price'] * 1000
    url = f'https://api.waxpeer.com/v1/buy-one-p2p?api={WAXPEER_API_KEY}&item_id={item_id}&token={STEAM_TOKEN}&price={item_price}&partner={STEAM_PARTNER}'

    response = requests.get(url=url, headers=HEADERS)

    print(response)


