from robot.api.deco import keyword
from robot.api.logger import info, debug
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.constants import TIMEOUT


class ElementNotFound(Exception):
    pass


class Browser:
    def __init__(self, driver, name):
        self.driver: WebDriver = driver
        self.name = name

    def _find_element_or_raise(self, by, locator) -> WebElement:
        info(f'Searching element {by!r} {locator!r}')
        if element := self.driver.find_element(by, locator):
            return element
        else:
            raise ElementNotFound(f'Failed to find element {by!r} {locator!r}!')

    @keyword(name='Find Element')
    def find_element(self, by, locator):
        return self._find_element_or_raise(by, locator)

    @keyword(name='Wait until element')
    def wait_until_element(self, by, locator):
        info(f'Waiting for {by!r} {locator!r}')
        if element := WebDriverWait(self.driver, TIMEOUT).until(EC.presence_of_element_located((by, locator))):
            debug(f'Successfully located {by!r} {locator!r}')
            return element
        else:
            raise ElementNotFound(f'Failed to find element {by!r} {locator!r}!')

    @keyword(name='Close browser')
    def close_browser(self):
        self.driver.quit()

    @keyword(name='Get location')
    def get_location(self):
        return self.driver.current_url

    @keyword(name='Go to')
    def go_to(self, url):
        info(f'Loading {url}')
        self.driver.get(url)

    @keyword(name='Input text')
    def input_text(self, by, locator, text):
        self._find_element_or_raise(by, locator).send_keys(text)
        info(f'Sending {text!r} to {by!r} {locator!r}')

    @keyword(name='Click element')
    def click_element(self, by, locator):
        self._find_element_or_raise(by, locator).click()
        info(f'Clicking {by!r} {locator!r}')

    @keyword(name='Wait until visible')
    def wait_until_visible(self, by, locator):
        info(f'Waiting until {by!r} {locator!r} is visible')
        return WebDriverWait(self.driver, TIMEOUT).until(EC.visibility_of_element_located((by, locator)))

    @keyword(name='Capture page screenshot')
    def capture_page_screenshot(self, file_name):
        image_path = file_name + '.png'
        self.driver.save_screenshot(image_path)
        info(f'<img src="{image_path}">', html=True)

    def find_elements(self, by, locator):
        info(f'Searching all elements by {by!r} {locator!r}')
        return self.driver.find_elements(by, locator)
