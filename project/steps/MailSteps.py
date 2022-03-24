import re
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage

import requests
from robot.api.deco import keyword
from robot.api.logger import info
from selenium.webdriver.remote.webelement import WebElement
from smart_assertions import soft_assert, verify_expectations

from config.constants import MESSAGE_PATH, SMTP_SERVER, SSL_PORT
from config.mail_credentials import MAIL_PASSWORD, MAIL_LOGIN
from project.page_objects.yopmail_page import YopMailPageObject
from utils.browser_manager.browser import Browser
from project.message.message import Message
from project.message.message_helpers import MessageHelper
from utils.waitutils.waitutils import WaitUtils

YOPMAIL_URL = "https://yopmail.com/"
YOPMAIL_KEYS = "qa.automation1190"
YOPMAIL_GO_BUTTON_LOCATOR = 'xpath', '//div[@id="refreshbut"]'
YOPMAIL_YCTPINPUT_LOCATOR = 'xpath', '//input[@class="ycptinput"]'
YOPMAIL_REFRESHBUT_LOCATOR = 'xpath', '//div[@id="refreshbut"]'
YOPMAIL_BNAME_LOCATOR = 'xpath', '//div[@class="bname"]'
YOPMAIL_INBOX_LOCATOR = 'xpath', '//div[@class="mctn"]/div[@class="m"]'
YOPMAIL_MESSAGE_SUBJECT_LOCATOR = 'xpath', '//div[contains(@class, "ellipsis")]'
YOPMAIL_MESSAGE_FROMDATE_LOCATOR = 'xpath', '//div[contains(@class, "md text")]'
YOPMAIL_MESSAGE_BODY_LOCATOR = 'xpath', '//div[@id="mail"]'

MAILTO_API_URL = "https://tempmail.plus/api/mails?"
MAILTO_MESSAGE_URL = "https://tempmail.plus/api/mails/"


class MailSteps:

    @staticmethod
    @keyword(name="Load Message From JSON")
    def load_message_from_json():
        parsed_message = MessageHelper.get_from_json(MESSAGE_PATH)
        today = datetime.now()
        parsed_message['date'] = today.strftime("%d/%m/%Y %H:%M")
        return Message(parsed_message['from'], parsed_message['to'], parsed_message['cc'],
                       parsed_message['subject'], parsed_message['text'], parsed_message['date'])

    @staticmethod
    @keyword(name="Prepare Message")
    def prepare_message(message: Message):
        return message.prepare()

    @staticmethod
    @keyword(name="Send Message")
    def send_message(message: EmailMessage):
        context = ssl.create_default_context()
        recipients = message.get("to").split(",") + message.get("cc").split(",")
        with smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT, context=context) as server:
            server.login(MAIL_LOGIN, MAIL_PASSWORD)
            server.sendmail(message.get("from"), recipients, message.as_string())

    @staticmethod
    @keyword(name="Open Yopmail")
    def open_yopmail(browser: Browser):
        browser.go_to(YOPMAIL_URL)
        browser.wait_until_element(*YOPMAIL_YCTPINPUT_LOCATOR)
        return YopMailPageObject(browser)

    @staticmethod
    @keyword(name="Enter Inbox")
    def enter_inbox(page: YopMailPageObject):
        email_input: WebElement = page.browser.find_element(*YOPMAIL_YCTPINPUT_LOCATOR)
        email_input.send_keys(YOPMAIL_KEYS)
        page.browser.click_element(*YOPMAIL_GO_BUTTON_LOCATOR)

    @staticmethod
    @keyword(name="Fetch Email")
    def fetch_email(page: YopMailPageObject):
        page.browser.wait_until_element(*YOPMAIL_BNAME_LOCATOR)
        recipient = page.browser.find_element(*YOPMAIL_BNAME_LOCATOR).text
        info("Looking for any emails in the inbox...")
        page.browser.driver.switch_to.frame('ifinbox')
        if fetched_emails := page.browser.find_elements(*YOPMAIL_INBOX_LOCATOR):
            fetched_emails[0].click()
            page.browser.driver.switch_to.default_content()
        else:
            raise Exception('Failed to locate any messages in the inbox!')
        page.browser.driver.switch_to.frame('ifmail')
        subject = page.browser.find_element(*YOPMAIL_MESSAGE_SUBJECT_LOCATOR).text
        f, d = page.browser.find_elements(*YOPMAIL_MESSAGE_FROMDATE_LOCATOR)
        from_dirty = f.text
        from_clean = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", from_dirty)
        _, dirty_date = d.text.split("\n")
        date = datetime.strptime(dirty_date, "%A, %B %d, %Y %I:%M:%S %p")
        body = page.browser.find_element(*YOPMAIL_MESSAGE_BODY_LOCATOR).text
        return Message(from_clean[0], recipient, "", subject, body, date.strftime("%d/%m/%Y %H:%M"))

    @staticmethod
    @keyword(name="Request Email")
    def request_email():
        payload = {"email": "qa.automation1191@mailto.plus", "limit": 20, "epin": ""}
        response = requests.get(MAILTO_API_URL, params=payload)
        first_id = str(response.json()['first_id'])
        if first_id == "0":
            raise Exception("Mailbox is empty! (first_id == 0)")
        message_url = MAILTO_MESSAGE_URL + first_id
        payload.pop("limit")
        response = requests.get(message_url, params=payload)
        md = response.json()
        date = datetime.strptime(md["date"], "%a, %d %b %Y %X %z")
        return Message(md["from_mail"], md["to"], "", md["subject"], md["text"], date.strftime("%d/%m/%Y %H:%M"))

    @staticmethod
    @keyword(name="Compare Fetched Emails")
    @WaitUtils.waituntiltrue
    def compare_fetched_emails(initial: Message, yopmail: Message, mailto: Message):
        info(f"Emails to compare:\nInitial message: {initial}\nYopmail: {yopmail}\nMailto: {mailto}")
        soft_assert(yopmail.sender in initial.sender, "Yopmail sender is not equal to initial message sender!")
        soft_assert(mailto.sender in initial.sender, "Mailto sender is not equal to initial message sender!")
        soft_assert(yopmail.to in initial.to, "Yopmail recipient is not in initial message recipients!")
        soft_assert(mailto.to in initial.to, "Mailto recipient is not in initial message recipients!")
        soft_assert(yopmail.subject in initial.subject, "Yopmail subject is not equal to initial message subject!")
        soft_assert(mailto.subject in initial.subject, "Mailto subject is not equal to initial message subject!")
        soft_assert(initial.text in yopmail.text, "Yopmail text does not contain initial message text!")
        soft_assert(initial.text in mailto.text, "Mailto text does not contain initial message text!")
        soft_assert(yopmail.date in initial.date, "Yopmail date does not match initial message date!")
        soft_assert(mailto.date in initial.date, "Mailto date does not match initial message date!")
        verify_expectations()
        return True
