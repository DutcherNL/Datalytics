class AlertMessage:
    code = None
    id = None
    room_id = None

    expected_vars = ['dt_start', 'dt_last_update', 'avg_value']

    def __init__(self, code, id, **kwargs):
        self.code = code
        self.id = id
        self.message_vars = {}

        for message_var in self.expected_vars:
            if message_var not in kwargs.keys():
                raise KeyError(f"Expected a value for '{var}', but this was not in the message")
            self.message_vars[message_var] = kwargs[message_var]


class AlertInterface:
    """ An interface class for the storage and retieval of alerts """

    def create_new_alert(self, code=None, room=None, **kwargs):
        pass

    def update_alert(self, code=None, room=None, timestamp=None, close=False):
        pass

    def _close_alert(self, code=None, room=None, timestamp=None):
        pass