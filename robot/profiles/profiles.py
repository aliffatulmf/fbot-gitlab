import os
import platform
import subprocess
from pathlib import Path
from zipfile import ZipFile
import subprocess

from robot import PROFILES_DIR, separator


def make_profile(name):                      
    user_profile = str(PROFILES_DIR) + f'{separator}fbot.{name.replace(" ", "_")}'
    current_path = Path(__file__).resolve().parent

    if not os.path.exists(user_profile):
        with ZipFile(str(current_path) + '/default.zip') as zipper:
            zipper.extractall(user_profile)
            return user_profile
    else:
        raise Exception('Profile exists')

def login_session(profile, linux_browser=None):
    """
    args:
        linux_browser:  ('chrome', 'chromium (default)', 'firefox')
    """

    argument = f'--user-data-dir={profile}'
    url = 'https://m.facebook.com/'
    win_pf = f'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    lin_pf = subprocess.getoutput('which google-chrome-stable')
    print(profile)

    sysOS = platform.system()
    
    if sysOS == 'Windows':
        subprocess.call([win_pf, argument, url])
    elif sysOS == 'Linux':
        subprocess.call([lin_pf, argument, url])
