import json


class MessageHelper:

    @staticmethod
    def get_from_json(path):
        with open(path, 'r', encoding='utf-8') as message:
            read_message = json.load(message)
        return read_message
