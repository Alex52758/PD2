
from datetime import datetime

import datetime

class Message(object):
    def __init__(self, id, text, date=datetime.datetime.now(), reciever="broadcast") -> None:
        self.id = id
        self.text = text
        self.date = date # todo: fix to format HH:MM:SS YYYY
        self.reciever = reciever
        
    
    def __repr__(self) -> dict:
        return {
            'id': self.id,
            'text': self.text,
            'date': self.date
        }