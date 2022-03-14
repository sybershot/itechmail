import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage

from robot.api.deco import keyword

from config.constants import MESSAGE_PATH, SMTP_SERVER, SSL_PORT
from project.utils.message import Message
from project.utils.message_helper import MessageHelper


class MailSteps:

    @staticmethod
    @keyword(name="Load message from JSON")
    def load_message_from_json():
        parsed_message = MessageHelper.get_from_json(MESSAGE_PATH)
        today = datetime.now()
        parsed_message['date'] = today.strftime("%d/%m/%Y %H:%M")
        return Message(parsed_message['from'], parsed_message['to'], parsed_message['cc'],
                       parsed_message['subject'], parsed_message['text'], parsed_message['date'])

    @staticmethod
    @keyword(name="Serialize message")
    def serialize_message(message: Message):
        return message.serialize()

    # @staticmethod
    # @keyword(name="Deserialize message")
    # def deserialize_message(message: Message):
    #     return message.deserialize()

    @staticmethod
    @keyword(name="Send message")
    def send_message(message: EmailMessage):
        context = ssl.create_default_context()
        password = input("Enter the password: ")
        recipients = message.get("to").split(",") + message.get("cc").split(",")
        with smtplib.SMTP_SSL(SMTP_SERVER, SSL_PORT, context=context) as server:
            server.login("qa.automation@mail.ru", password)
            server.sendmail(message.get("from"), recipients, message.as_string())


