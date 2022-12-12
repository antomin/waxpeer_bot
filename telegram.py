import requests

from settings import TG_TOKEN, CHAT_ID


def send_to_channel(message):
    requests.get(f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}')
