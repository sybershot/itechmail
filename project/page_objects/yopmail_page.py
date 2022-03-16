from project.page_objects.base_page import BasePage
from utils.browser_manager.browser import Browser

INBOX_LOCATOR = 'xpath', '//div[@class="mctn"]'


class YopMailPageObject(BasePage):

    def __init__(self, browser: Browser):
        super().__init__(browser)

    @classmethod
    def inbox_menu(cls):
        return INBOX_LOCATOR
