from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart

from serialization import Serializable


@dataclass
class Message(Serializable):
    sender: str
    to: str
    cc: str
    subject: str
    text: str
    date: str

    def serialize(self):
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.to
        message['CC'] = self.cc
        message['Subject'] = self.subject
        message['Text'] = self.text + '\n' + self.date
        return message

    def deserialize(self):
        pass
