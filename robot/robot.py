import csv
import os
import sys
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

ROOT = 'div[data-testid="Keycommand_wrapper_ModalLayer"]'


class Category:
    # Home & Garden
    TOOLS = 2
    FURNITURE = 3
    HOUSEHOLD = 4
    GARDEN = 5
    APPLIANCES = 6

    # Entertainment
    VIDEO_GAMES = 8
    BOOKS_MOVIES_MUSIC = 9

    # Clothing & Accessories
    BAGS_LUGGAGE = 11
    WOMENS_CLOTHING_SHOES = 12
    MENS_CLOTHING_SHOES = 13
    JEWELRY_ACCESSORIES = 14

    # Family
    HEALTH_BEAUTY = 16
    PET_SUPPLIES = 17
    BABY_KIDS = 18
    TOYS_GAMES = 19

    # Electronics
    ELECTRONICS_COMPUTERS = 21
    MOBILE_PHONES = 22

    # Hobbies
    BICYCLES = 24
    ARTS_CRAFTS = 25
    SPORTS_OUTDOORS = 26
    AUTO_PARTS = 27
    MUSICAL_INSTRUMENTS = 28
    ANTIQUES_COLLECTIBLES = 29

    # Classifieds
    GARAGE_SALE = 31
    MISCELLANEOUS = 32

    def __init__(self, driver):
        self.driver = driver
        self.driver.find_element(
            By.CSS_SELECTOR,
            'div[aria-label="Marketplace"] > div.dati1w0a:nth-child(5)').click(
            )
        sleep(5)
        self.root = self.driver.find_element(By.CSS_SELECTOR, ROOT)

    def _elem(self, number):
        el = 'div[data-visualcompletion="ignore-dynamic"]:nth-child({num})'
        return el.format(num=number)

    def open(self, param):
        # fix bug 23 sep 2020
        driver.find_element(By.CSS_SELECTOR, 'div[role="dialog"]')
        driver.find_element(By.CSS_SELECTOR, self._elem(param)).click()


class Condition:
    NEW = 1
    LIKE_NEW = 2
    GOOD = 3
    FAIR = 4

    def __init__(self, driver):
        self.driver = driver
        self.driver.find_element(
            By.CSS_SELECTOR,
            'div[aria-label="Marketplace"] > div.dati1w0a:nth-child(6)').click(
            )
        sleep(5)
        self.root = self.driver.find_element(By.CSS_SELECTOR, ROOT)

    def open(self, param):
        driver.find_element(By.CSS_SELECTOR, 'div[data-pagelet="root"]')
        driver.find_element(By.CSS_SELECTOR, 'div > div > div > div > div')
        driver.find_element(
            By.CSS_SELECTOR,
            'div[role="menuitemradio"]:nth-child({number})'.format(
                number=param)).click()


class Point:
    def __init__(self, filename: str):
        self.file = filename

    @staticmethod
    def remove_empty(obj: list):
        tmp = []
        for ls in obj:
            if ls != '':
                tmp.append(ls)

        return tmp

    def data2point(self):
        with open(self.file, mode='r', encoding='utf-8') as f:
            return [x for x in csv.DictReader(f)]

    def image2point(self):
        with open(self.file, mode='r', encoding='utf-8') as f:
            v = csv.reader(f)
            header = []
            pass_1 = []
            pass_2 = []

            # img_1 - img_10
            for x in v:
                header.append(x[5:15])

            # remove empty string
            # remove header
            for x in header[1:]:
                pass_1.append(self.remove_empty(x))

            # add new line
            for x in pass_1:
                tmp = []
                for y in x:
                    tmp.append(y)
                    tmp.append('\n')
                pass_2.append(tmp)

            # make list
            for x in range(len(pass_2)):
                if pass_2[x][-1:][0] == '\n':
                    del pass_2[x][-1:]

        return pass_2


def main(
    driver,
    img_value,
    title_value,
    price_value,
    category,
    condition,
    description,
    tags_value,
    location_value,
):
    # START IMAGE SECTION
    img = driver.find_element(
        By.CSS_SELECTOR,
        'div[aria-label="Marketplace"] > div.dati1w0a:nth-child(2)')
    img.find_element(
        By.CSS_SELECTOR,
        'label:nth-child(2) > input[accept^="image"]').send_keys(img_value)
    sleep(5)
    # END IMAGE SECTION

    # START TITLE SECTION
    title = driver.find_element(
        By.CSS_SELECTOR,
        'div[aria-label="Marketplace"] > div.discj3wi:nth-child(3)')
    title.find_element(By.CSS_SELECTOR, 'div > input').send_keys(title_value)
    sleep(5)
    # END TITLE SECTION

    # START PRICE SECTION
    price = driver.find_element(
        By.CSS_SELECTOR,
        'div[aria-label="Marketplace"] > div.discj3wi:nth-child(4)')
    price.find_element(By.CSS_SELECTOR, 'div > input').send_keys(price_value)
    sleep(5)
    # END PRICE SECTION

    # START CATEGORY SECTION
    cat = Category(driver)
    cat.open(category)
    sleep(5)
    # END CATEGORY SECTION

    # START CONDITION SECTION
    con = Condition(driver)
    con.open(condition)
    sleep(5)
    # END CONDITION SECTION

    # START DESCRIPTION SECTION
    driver.find_element(
        By.CSS_SELECTOR, 'div.discj3wi:nth-child(8) > div:nth-child(1) > \
            div:nth-child(1) > label:nth-child(1) > \
                div:nth-child(1) > div:nth-child(1)')
    driver.find_element(By.TAG_NAME, 'textarea').clear()

    desc = driver.find_element(By.CSS_SELECTOR, 'div.discj3wi:nth-child(8)')
    desc.find_element(By.CSS_SELECTOR, 'div > textarea').send_keys(description)
    sleep(5)
    # END DESCRIPTION SECTION

    # START TAGS SECTION
    driver.find_element(
        By.CSS_SELECTOR, 'div.discj3wi:nth-child(9) > div:nth-child(1) > \
            div:nth-child(1) > div:nth-child(1) > \
                label:nth-child(1) > div:nth-child(1) > \
                    div:nth-child(1) > div.gcieejh5:nth-child(2) \
                        > div > textarea').clear()
    tags = driver.find_element(
        By.CSS_SELECTOR, 'div.discj3wi:nth-child(9) > div:nth-child(1) > \
            div:nth-child(1) > div:nth-child(1) > label:nth-child(1) > \
                div:nth-child(1) > div:nth-child(1) > \
                    div.gcieejh5:nth-child(2)')
    for tag in tags_value.split('|'):
        tags.find_element(By.CSS_SELECTOR,
                          'div > textarea').send_keys(tag, Keys.ENTER)
        sleep(1)
    sleep(5)
    # END TAGS SECTION

    # START LOCATION SECTION
    location = driver.find_element(By.CSS_SELECTOR,
                                   'div.discj3wi:nth-child(10)')
    location.find_element(By.CSS_SELECTOR,
                          'div > input').send_keys(location_value)
    sleep(3)
    selection_location = '#mount_0_0 > div > div:nth-child(1) > \
    div.rq0escxv.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb \
        > div > div > div:nth-child(2) > \
            div > div > div'

    selection = driver.find_element(By.CSS_SELECTOR, selection_location)
    selection.find_element(By.CSS_SELECTOR,
                           'div > div > ul > li:nth-child(1)').click()
    sleep(5)
    # END LOCATION SECTION

    # START LISTING SECTION
    driver.find_element(
        By.CSS_SELECTOR,
        'div[aria-label="Marketplace"] > div > span > div:nth-child(1)').click(
        )
    sleep(3)
    driver.find_element(
        By.CSS_SELECTOR,
        '#mount_0_0 > div > div:nth-child(1) > div.rq0escxv.l9j0dhe7.du4w35lb > \
        div.rq0escxv.l9j0dhe7.du4w35lb > div > div > \
            div:nth-child(2) > div > div > div').click()
    sleep(5)
    # END LISTING SECTION

    # START PUBLISH SECTION
    publish = '#mount_0_0 > div > div:nth-child(1) > div.rq0escxv.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.pfnyh3mw.jifvfom9.gs1a9yip.owycx6da.btwxx1t3.buofh1pr.dp1hu0rb > div.rq0escxv.l9j0dhe7.tkr6xdv7.j83agx80.cbu4d94t.pfnyh3mw.d2edcug0.hpfvmrgz.dp1hu0rb.rek2kq2y.o36gj0jk.oali7pvx > div > div.dati1w0a.ihqw7lf3.hv4rvrfc.discj3wi.taijpn5t.pfnyh3mw.j83agx80.l6v480f0.bp9cbjyn > div'
    driver.find_element(By.CSS_SELECTOR, publish).click()
    sleep(5)
    # END PUBLISH SECTION


def start(driver, profile_path, filename):
    url = 'https://www.facebook.com/marketplace/create/item'
    try:

        if not os.path.exists(filename):
            raise Exception('csv not found')

        # read csv
        p = Point(filename)
        data = p.data2point()
        image = p.image2point()

        # data loop
        for x in range(len(data)):
            driver.get(url)
            sleep(10)
            main(driver=driver,
                 img_value=image[x],
                 title_value=data[x]['title'],
                 price_value=data[x]['price'],
                 category=data[x]['category'],
                 condition=data[x]['condition'],
                 description=data[x]['description'],
                 tags_value=data[x]['tags'],
                 location_value=data[x]['location'])
    except Exception as e:
        print(e)
        driver.quit()


if __name__ == "__main__":
    # profile = sys.argv[1]
    files = 'tmp.csv'
    opt = webdriver.FirefoxOptions()
    profile = webdriver.FirefoxProfile(
        '/home/eva/.mozilla/firefox/hqcb5rcq.dev')
    path = './geckodriver'

    driver = webdriver.Firefox(firefox_profile=profile,
                               executable_path=path,
                               options=opt)
    try:
        start(driver, profile, files)
    except Exception as e:
        print(e)

    driver.quit()