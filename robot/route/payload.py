import csv
from time import sleep

from fbot.settings import BASE_DIR
from robot import DRIVER_DIR, FACEBOOK_URL
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

repeat_range = 5

class Image2List:
    def __init__(self, filename: str):
        self.file = filename

    @staticmethod
    def remove_empty(obj: list):
        tmp = []
        for ls in obj:
            if ls != '':
                tmp.append(ls)

        return tmp

    def text_to_list(self):
        with open(self.file, mode='r', encoding='utf-8') as f:
            return [x for x in csv.DictReader(f)]

    def image_to_list(self):
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

class BasePayload(object):
    def __init__(self, profile):
        """
        args:
            profile:    profile path
        """
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-data-dir={profile}')
        options.add_argument('stable-release-mode')
        options.add_argument('start-maximized')
        options.add_argument('silent-debugger-extension-api')
        options.add_argument('disable-notifications')
        
        self.driver = webdriver.Chrome(
            chrome_options=options,
            executable_path=DRIVER_DIR
        )
        self.counter = 2

    def index_selector(self, by=None, counter=None):
        by = By.CSS_SELECTOR if by == None else by
        counter = self.counter if counter == None else counter
        self.driver.implicitly_wait(30)
        element = f'div[aria-label="Marketplace"] > div:nth-child(1) > div:nth-child({counter})'
        index = self.driver.find_element(by, element)
        return index

    def image_field(self, img):
        img_parent = self.index_selector(By.CSS_SELECTOR, self.counter)
        img_parent.find_element_by_css_selector('label:nth-child(2) > input[accept^="image"]').send_keys(img)
        self.counter += 1

    def text_field(self, title: str, price: int):
        text = self.index_selector(By.CSS_SELECTOR, self.counter).find_element_by_css_selector('div > input')
        text.send_keys(title, Keys.TAB, price)
        self.counter += 2

    def category_field_legacy(self, name: str):
        """old model
        args:
            name:   category name
        
        return:
            None
        """
        def repeater(name):
            row = 1
            self.index_selector(By.CSS_SELECTOR, 5).click()
            while True:
                self.driver.implicitly_wait(5)
                idx = self.driver.find_element_by_xpath(f'//div[@data-visualcompletion="ignore-dynamic"][{row}]')
                if str(idx.text).lower() == name.lower():
                    idx.click()
                    self.counter += 1
                    return 1
                row += 1

        for repeat in range(repeat_range):
            r = repeater(name)
            if r:
                break

    def category_field(self, name: str):
        index = self.index_selector(By.CSS_SELECTOR, self.counter)
        self.driver.implicitly_wait(30)
        focus = index.find_element(By.CSS_SELECTOR, 'div > input')
        focus.clear()
        focus.send_keys('Pet')
        self.driver.find_element(By.CSS_SELECTOR, 'ul[role="presentation"] > li:nth-child(1)')
        self.driver.implicitly_wait(30)
        focus.send_keys(Keys.ARROW_DOWN, Keys.ENTER)
        self.counter += 1

    def condition_field(self, text):
        status = {
            'NEW': 1,
            'LIKE_NEW': 2,
            'GOOD': 3,
            'FAIR': 4
        }
        row = status.get(text.replace(' ', '_').upper())
        
        for repeat in range(repeat_range):
            if repeat == repeat_range-1:
                raise NoSuchElementException(self.driver)
            self.index_selector().click()
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_css_selector(f'div[role="menuitemradio"]:nth-child({row})').click()
            self.counter += 1
            break

    def optional_field(self):
        def menu_radio(rows):
            rows.click()
            self.driver.find_element_by_css_selector('div[role="menuitemradio"]:nth-child(1)').click()
            self.counter += 1
            return 1
        
        def menu_input(rows):
            row = rows.find_element_by_css_selector('input')
            row.clear()
            row.send_keys('Tidak Ada')
            self.counter += 1
            return 1
        
        def description(rows):
            if rows.find_element_by_css_selector('span').text == 'Description':
                return 0

        options = menu_radio, menu_input, description
        rows = self.index_selector()

        for func in options:
            try:
                self.driver.implicitly_wait(5)
                return func(rows)
            except:
                continue

    def description_field(self, text):
        self.driver.implicitly_wait(5)
        textarea = self.driver.find_element_by_css_selector(f'div[aria-label="Marketplace"] > div:nth-child(1) > div:nth-child({self.counter})').find_element_by_tag_name('textarea')
        textarea.clear()
        textarea.send_keys(text)
        self.counter += 1

    def tags_field(self, tags):
        tag_parent = self.index_selector(By.CSS_SELECTOR)
        self.driver.implicitly_wait(5)
        tag_parent.find_element_by_css_selector('div > textarea').clear()

        for item in tags.split('|'):
            tag_parent.find_element_by_css_selector('div > textarea').send_keys(item, Keys.ENTER)
            sleep(.7)
        self.counter += 1

    def location_field(self, text):
        location = self.index_selector(By.CSS_SELECTOR, self.counter).find_element_by_css_selector('div > input')
        self.driver.implicitly_wait(10)
        location.send_keys((Keys.CONTROL, 'a'), Keys.CLEAR)
        location.send_keys(text)
        sleep(15)
        location.send_keys(Keys.ARROW_DOWN, Keys.ENTER)
        self.counter += 1

    def availability_field(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_css_selector(f'div[aria-label="Marketplace"] > div:nth-child(1) > div:nth-child({self.counter}) > span:nth-child(1) > div:nth-child(1)').click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_css_selector('div[role="menuitemradio"]:nth-child(2)').click()
        self.counter += 1

    def publish(self):
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[4]').click()


def triggerByThread(profile: str, filepath: str):
    """
    args:
        profile: user profile location
        filepath: datset location
        timing: loop delay
    """
    try:
        payload = BasePayload(profile)
        payfile = Image2List(filepath)

        img = payfile.image_to_list()
        text = payfile.text_to_list()

        for i, t in zip(img, text):
            payload.counter = 2
            payload.driver.get(FACEBOOK_URL + 'marketplace/create/item')
            sleep(5)

            payload.image_field(i)
            payload.text_field(t['title'], t['price'])
            payload.category_field_legacy(t['category'])
            payload.condition_field(t['condition'])
            while True:
                if not payload.optional_field():
                    break            
            payload.description_field(t['description'])
            payload.tags_field(t['tags'])
            payload.location_field(t['location'])
            payload.availability_field()
            payload.publish()

            sleep(60) 
    except Exception as e:
        raise e
    payload.driver.quit()
