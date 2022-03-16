from utils.browser_manager.browser import Browser


class BasePage:
    def __init__(self, browser: Browser):
        self.browser = browser

    def save_screenshot(self, fname):
        self.browser.capture_page_screenshot(fname)
