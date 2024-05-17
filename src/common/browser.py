from selenium import webdriver

import time
from selenium.webdriver.chrome.options import Options as ChromeOptions
from .constant.browser_const import BrowserConst
from .constant.proxy_const import proxies


class ChromeBrowser(webdriver.Chrome):
    browser_const = BrowserConst()

    def __init__(self, options: ChromeOptions = None, is_headless: bool = True):
        options = options if options else self._default_header(is_headless)
        super().__init__(options=options)

    def _default_header(self, is_headless):
        opts = ChromeOptions()
        opts.add_argument(f"user-agent={self.browser_const.user_agent}")
        # opts.add_argument("--proxy-server={}".format(proxies[0]))
        if is_headless:
            opts.add_argument('--headless')

        opts.add_argument('--no-sandbox')
        opts.add_argument('--disable-dev-shm-usage')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--disable-software-rasterizer')
        opts.add_argument('--remote-debugging-port=9222')
        opts.add_argument("disable-infobars")
        return opts
