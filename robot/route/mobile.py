import csv
import datetime
import glob
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import time

from django.http import JsonResponse
from fbot.settings import BASE_DIR
from robot.utils import Util
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


class Driver:
    def __init__(self, profile):
        options = webdriver.ChromeOptions()

        if pathlib.Path(profile).exists():
            options.add_argument(f"user-data-dir={profile}")
            options.add_argument("--disable-logging")
            options.add_argument("--disable-in-process-stack-traces")
            options.add_argument("--log-level=3")
            options.add_argument("--noerrdialogs")

        self.driver = webdriver.Chrome(executable_path=Util.driver_dir, options=options)


class Mobile(Driver):
    def __init__(self, profile):
        super().__init__(profile)

    def main(self, data):
        driver = self.driver
        driver.get("https://m.facebook.com/marketplace/selling/item")

        # Images
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'a[data-sigil="MBackNavBarClick"]')
                )
            )
        except:
            driver.quit()

        images_itter = Util().image_folder(data["IMAGES"])
        for img in images_itter:
            driver.implicitly_wait(5)
            image = driver.find_element_by_css_selector(
                'input[name="photos-input"][accept="image/*"]'
            )
            image.send_keys(img)

        # Title
        driver.implicitly_wait(5)
        time.sleep(3)
        title = driver.find_element_by_name("title")
        title.send_keys(data["NAME"])

        # Price
        driver.implicitly_wait(5)
        time.sleep(3)
        price = driver.find_element_by_name("price")
        price.send_keys(data["PRICE"])

        # Category
        driver.implicitly_wait(5)
        time.sleep(3)
        category = driver.find_element_by_xpath('//*[@name="category"]//parent::div')
        category.click()

        row = 1
        while True:
            try:

                driver.implicitly_wait(5)
                lrow = driver.find_element_by_xpath(
                    f'//div[@id="modalDialogView"]/div/div/div[{row}]'
                )

                if re.search(data["CATEGORY"], lrow.text):
                    lrow.click()
                    break

                row += 1

            except NoSuchElementException:
                break

        # Location
        driver.implicitly_wait(5)
        time.sleep(3)
        location = driver.find_element_by_xpath('//*[@name="location"]//parent::div')
        location.click()

        time.sleep(3)
        try:
            search = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/div/div[2]/div/div/div[1]/div[1]/input",
                    )
                )
            )
            search.send_keys(data["LOCATION"])
        except:
            driver.quit()

        driver.implicitly_wait(5)
        time.sleep(3)
        try:
            row = driver.find_element_by_xpath(
                '//div[@id="nt-typeahead-results-view"]/div[@id="0"]'
            )
            row.click()
        except:
            pass

        # Description
        driver.implicitly_wait(5)
        time.sleep(3)
        desc = driver.find_element_by_name("description")
        desc.clear()
        desc.send_keys(data["DESCRIPTION"])

        # Post
        try:
            post = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//form[@method="post"]/div[2]/div/div/div[7]/div[3]')
                )
            )
            time.sleep(3)
            post.click()
        except:
            driver.exit()

        time.sleep(10)
        try:
            identifier = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[@data-sigil="MBackNavBarClick"]')
                )
            )

            if re.search("Marketplace", identifier.text):
                return driver.current_url
        except:
            driver.quit()

    def exit(self):
        self.driver.quit()


LOGS = pathlib.Path(BASE_DIR / "logs")


def interface(profile, pathfile):
    # ../BASE_DIR/logs/
    file_dir = str(LOGS / pathfile.filename.split(sep=".")[0]) + ".csv"

    with open(file_dir, mode="a", newline="", encoding="utf-8") as flog:
        linewriter = csv.writer(flog, delimiter=",")

        _time = datetime.datetime.now()
        _name = pathfile.name
        linewriter.writerow([f"{_time} {_name}"])

        try:
            with open(pathfile.path, mode="r", encoding="utf-8") as pf:
                rows = csv.DictReader(pf)
                mobile = Mobile(profile=profile)
                data = []

                for row in rows:
                    data.append(row)

                for row in data:
                    cd = 60
                    url = mobile.main(row)

                    linewriter.writerow([url])

                    if row != data[-1]:
                        while cd:
                            cd -= 1
                            time.sleep(1)

                mobile.exit()
        except RuntimeError as e:
            raise e
