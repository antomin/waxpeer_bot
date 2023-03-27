import os
# System options
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADLESS = False

#
CACHE_ENABLE = False

TG_TOKEN = ''
CHAT_ID = ''

STICKER_SEARCH_STRING = ''

EXCEPTIONS = [
    '',
]

STICKERS_AUTOBUY_TERMS = {
    250: 500,
    100: 250,
    50: 100,
    20: 50,
    10: 30,
}

FLOAT_AUTOBUY_TERMS = {
    'Consumer Grade': (0.0001, 50),
    'Mil-Spec Grade': (0.0001, 50),
    'Industrial Grade': (0.0001, 50),
    'Restricted': (0.0001, 50),
    'Classified': (0.001, 30),
    'Covert': (0.001, 30)
}

FLOAT_NOTIFICATION_TERMS = {
    'Consumer Grade': 0.001,
    'Mil-Spec Grade': 0.001,
    'Industrial Grade': 0.001,
    'Restricted': 0.001,
    'Classified': 0.01,
    'Covert': 0.01
}
