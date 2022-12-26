import os

# System options
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADLESS = False
CACHE_ENABLE = True

TG_TOKEN = '5626409225:AAGd_x4-uKVal507aOGW8cq2Mva3WT8nR20'
CHAT_ID = '-1001824416043'

WAXPEER_API_KEY = '3f7d605c4fa4c037160e726ac11c78e7fa3c59f817a2033bb11504a867c5ce95'
STEAM_PARTNER = 1226607877
STEAM_TOKEN = 'LSQk0Cb5'

STICKER_SEARCH_STRING = ''

NAME_EXCEPTIONS = [
    'Souvenir',
    'Сувенир',
    'Glock-18 Gamma Doppler',
]

MIN_STICKERS_SUM = 30

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

KNIFE_COVERT_LIST = {
    'items': [
        'Nomad Knife',
        'Skeleton Knife',
        'Survival Knife',
        'Paracord Knife',
        'Classic Knife',
        'Bayonet',
        'Bowie Knife',
        'Butterfly Knife',
        'Falchion Knife',
        'Flip Knife',
        'Gut Knife',
        'Huntsman Knife',
        'Karambit',
        'M9 Bayonet',
        'Navaja Knife',
        'Shadow Daggers',
        'Stiletto Knife',
        'Talon Knife',
        'Ursus Knife',
    ],
    'range': 0.001
}

GLOVES_COVERT_LIST = {
    'items': [
        'Bloodhound Gloves',
        'Broken Fang Gloves',
        'Driver Gloves',
        'Hand Wraps',
        'Hydra Gloves',
        'Moto Gloves',
        'Specialist Gloves',
        'Sport Gloves',
    ],
    'ranges': [
        (0.06, 0.10),
        (0.15, 0.20),
        (0.45, 0.46),
    ]
}
