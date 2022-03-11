import json

from jsonic import deserialize


class MessageHelper:

    @staticmethod
    def get_from_json(path):
        with open(path, 'r', encoding='utf-8') as message:
            read_message = json.load(message)
            deserialized_message = deserialize(read_message)
        return deserialized_message

