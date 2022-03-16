from dataclasses import dataclass
from email.message import EmailMessage

from serialization import Serializable


@dataclass
class Message(Serializable):
    sender: str
    to: str
    cc: str
    subject: str
    text: str
    date: str

    def prepare(self):
        message = EmailMessage()
        message.add_header("From", self.sender)
        message.add_header("To",  self.to)
        message.add_header("CC", self.cc)
        message.add_header("Subject", self.subject)
        body = self.text
        message.set_content(body)
        return message

    def serialize(self):
        return {"sender": self.sender, "to": self.to, "cc": self.cc,
                "subject": self.subject, "body": self.text, "date": self.date}
