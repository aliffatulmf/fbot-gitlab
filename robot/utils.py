import glob
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import (
    InvalidArgumentException,
    InvalidElementStateException,
    NoSuchElementException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Util:
    drivername = "chromedriver"
    base_dir = pathlib.Path().resolve()
    config_dir = base_dir / "config"
    driver_dir = str(config_dir / "driver" / drivername)
    files_dir = str(config_dir / "files")

    system = platform.system()
    arch = platform.architecture()[0]

    def image_folder(self, dir):
        """
        Read file in folder

        :Args:
            dir: folder location

        :Usage:
            image_folder('/home/dir')
        """
        path = str(pathlib.Path(dir) / "*")

        folder = glob.glob(path)
        item = []

        for file in folder:
            if re.search(".(png|jpg|jpeg)$", file):
                item.append(file)

        return item

    def driver_kill(self) -> None:
        """
        Kill driver process

        :Usage:

        :Args:
        """
        name = self.drivername

        if self.system == "Linux":
            subprocess.call(["pkill", name])
        elif self.system == "Windows":
            import wmi

            f = wmi.WMI()
            for process in f.Win32_Process():
                if process.name == name:
                    process.Terminate()

    def create(self, name, callback=None):
        full_path = self.config_dir / "profiles" / name
        if not full_path.exists():
            try:
                os.mkdir(str(full_path))
                if callback != None:
                    callback(full_path)
            except:
                pass

        return str(full_path)

    def run(self, path):
        if path.exists():
            path = str(path)
            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir={path}")

            driver = webdriver.Chrome(executable_path=self.driver_dir, options=options)
            driver.get("https://m.facebook.com/")
            try:
                WebDriverWait(driver, 300).until(EC.title_is("Facebook"))
            finally:
                driver.quit()

    def delete(self, path) -> bool:
        """
        return true if path is not exists
        return false if path is exists
        """

        def check_dir(path):
            if pathlib.Path(path).exists():
                return False
            else:
                return True

        if pathlib.Path(path).exists():
            shutil.rmtree(path)
        return check_dir(path)

    def remove_file(self, filename):
        file = pathlib.Path(filename)
        file_status = file.exists()

        if file_status:
            os.remove(str(file))

        return file_status


class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def compass(value):
    return Namespace(**value)
