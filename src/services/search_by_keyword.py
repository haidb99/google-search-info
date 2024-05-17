import json
import random
from io import BytesIO

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import os
from hashlib import sha256
from selenium.webdriver.common.by import By
from ..common import ChromeBrowser
import urllib.parse
import time
from ..models.search_item_model import SearchItemModel


class GoogleSearchInfo:
    def __init__(self, key_word: str):
        self.key_word = str(key_word).strip()
        self.browser = ChromeBrowser(is_headless=True)
        self.path_save = "data/keyword_" + sha256(self.key_word.lower().encode('utf-8')).hexdigest() + ".json"

        if not os.path.exists("data"):
            os.makedirs("data")

    @property
    def url(self):
        return "https://www.google.com/maps/search/" + urllib.parse.quote(self.key_word)

    def get_data_by_page(self, page=1, limit=20):
        if not os.path.isfile(self.path_save):
            self.crawl()

        total = 0
        data = []
        with open(self.path_save, "r", encoding='utf-8') as f:
            for line in f:
                total += 1
                if (total > limit * (page - 1)) and (total <= limit * page):
                    data.append(json.loads(line))

        return {
            "data": data,
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
                "key_word": self.key_word
            }
        }

    def export_excel(self):
        if not os.path.isfile(self.path_save):
            self.crawl()

        df = pd.read_json(self.path_save, lines=True, encoding='utf-8')
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

        output.seek(0)
        return output
    def crawl(self):
        soup = self._load_website()
        list_div = soup.find_all(self._find_div_item)
        data = []
        for div_item in list_div:
            temp = self._extract_item(div_item)
            if temp != {}:
                data.append(temp)
        self._save_data(data)

    def _load_website(self):
        self.browser.get(self.url)
        time.sleep(5)
        element = self.browser.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
        last_height = self.browser.execute_script("return arguments[0].scrollHeight;", element)
        while True:
            print("Đang load...")
            self.browser.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", element)
            time.sleep(random.uniform(1, 3))
            new_height = self.browser.execute_script("return arguments[0].scrollHeight;", element)
            if new_height == last_height:
                break

            last_height = new_height

            # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = BeautifulSoup(element.get_attribute('outerHTML'), 'html.parser')
        return soup

    def _find_div_item(self, tag):
        return tag.name == 'div' and tag.find('a', recursive=False)

    def _validate_phone_number(self, phone_number):
        for r in phone_number:
            if r not in '+0123456789 ':
                return False
        return True

    def _extract_item(self, div_item):
        item = SearchItemModel()
        item.key_word = self.key_word
        item.url = div_item.find('a').attrs['href']

        try:
            item.name = div_item.find("div", attrs={"class": "fontHeadlineSmall"}).text.strip()
        except:
            return {}

        div_temp = div_item.find("div", attrs={"class": "fontBodyMedium"})
        try:
            item.rating = (
                div_temp
                .find("span", attrs={"class": "fontBodyMedium"})
                .find("span")
                .attrs["aria-label"].strip()
            )
        except:
            pass

        try:
            item.address = (
                div_temp
                .find_all("div", recursive=False)[-1]
                .find_all("div", recursive=False)[0]
                .find_all(lambda tag: tag.name == "span" and len(tag.find_all("span")) == 0)[-1]
                .text.strip()
            )
        except:
            pass

        try:
            phone_number = (
                div_temp
                .find_all("div", recursive=False)[-1]
                .find_all("div", recursive=False)[-1]
                .find_all(lambda tag: tag.name == "span" and len(tag.find_all("span")) == 0)[-1]
                .text.strip()
            )
            if self._validate_phone_number(phone_number):
                item.phone_number = phone_number
        except:
            pass
        # print(item.to_dict())
        return item.to_dict()

    def _save_data(self, data):
        with open(self.path_save, "w", encoding="utf-8") as file:
            for item in data:
                file.write(json.dumps(item) + "\n")


def dev():
    key_word = "Nhà thuốc Hà Nội"
    search = GoogleSearchInfo(key_word)
    # print(search.get_data_by_page(1, 5))
    search.export_excel()