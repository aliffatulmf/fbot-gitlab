import platform

from fbot.settings import BASE_DIR


def ossep():
    system = platform.system()

    if system == 'Windows':
        return '\\'
    elif system == 'Linux':
        return '/'

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def compass(value):
    return Namespace(**value)

separator = ossep()

CONFIG_DIR = BASE_DIR / 'config'
DRIVER_DIR = str(CONFIG_DIR / f'driver{separator}chromedriver')
PROFILES_DIR = str(CONFIG_DIR / 'profiles')
FACEBOOK_URL = 'https://www.facebook.com/'
FILES_DIR = str(CONFIG_DIR / f'files{separator}/')