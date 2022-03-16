from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager, EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.utils import ChromeType

from utils.browser_manager.drivermanager_config import DRIVERS_LOCATION


class UnsupportedBrowser(Exception):
    pass


class DriverFactory:
    @staticmethod
    def get_driver(browser_type):
        if browser_type == 'Chrome':
            driver = webdriver.Chrome(ChromeDriverManager(path=DRIVERS_LOCATION).install())
        elif browser_type == 'Firefox':
            driver = webdriver.Firefox(executable_path=GeckoDriverManager(path=DRIVERS_LOCATION).install())
        elif browser_type == 'Chromium':
            driver = webdriver.Chrome(
                ChromeDriverManager(path=DRIVERS_LOCATION, chrome_type=ChromeType.CHROMIUM).install())
        elif browser_type == 'IE':
            driver = webdriver.Ie(IEDriverManager(path=DRIVERS_LOCATION).install())
        elif browser_type == 'Edge':
            driver = webdriver.Edge(EdgeChromiumDriverManager(path=DRIVERS_LOCATION).install())
        elif browser_type == 'Opera':
            options = webdriver.ChromeOptions()
            options.add_argument('allow-elevated-driver')
            options.binary_location = DRIVERS_LOCATION
            driver = webdriver.Opera(executable_path=OperaDriverManager(path=DRIVERS_LOCATION).install(),
                                     options=options)
        else:
            raise UnsupportedBrowser(f'Browser {browser_type!r} is not supported')
        return driver
