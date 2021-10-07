import json
import os
import errno

from datalytics.utils import get_setting
from datalytics.messaging.models import AlertMessage



class JsonMessageFile:
    file_folder = 'json_alerts/'
    messages = []

    def __init__(self, file_name: str, message_code: str):

        # Setup file related data
        if not file_name.endswith('.json'):
            file_name += '.json'
        self.file_name = file_name

        self.file_location=get_setting('FILE_LOCATION')+self.file_folder
        if not os.path.exists(os.path.dirname(self.file_location)):
            try:
                os.makedirs(os.path.dirname(self.file_location))
            except OSError as exc: # Race condition check
                if exc.errno != errno.EEXIST:
                    raise

        # Setup content related data
        self.message_code=message_code

    @property
    def get_content(self):
        json_messages = []
        for message in self.messages:
            json_messages.append({
                'id': message.id,
                **message.message_vars
            })

        return {
            'code': self.message_code,
            'messages': json_messages,
        }


    def save(self):
        with open(self.file_location+self.file_name, 'w') as f:
            json.dump(self.get_content, f)

    def load(self):
        pass

    def add(self, message: AlertMessage):
        """ Adds a message to the storage device """
        self.messages.append(message)

    def update(self, message: AlertMessage):
        for i in range(len(self.messages)):
            if self.messages[i].id == message.id:
                self.messages[i] = message
                break
        else:
            raise KeyError(f"Message with id {message.id} was not in the list originally")
