


class CodeDataCommunication:

    TITLE = 1
    SHORT_TEXT = 2

    def __init__(self):
        self.texts = {}

    def register(self, code, title=None, short_text=None):
        data = self.texts.get(code, {})
        if title:
            data[self.TITLE] = title
        if short_text:
            data[self.SHORT_TEXT] = short_text

        self.texts[code] =  data

    def get_readable(self, code, data_type):
        return self.texts.get(code, {}).get(data_type, '-NOT REGISTERED-')


data_info = CodeDataCommunication()


data_info.register(
    'test',
    'Test event',
    'This is a test event'
)

data_info.register(
    'heat_upperlimit_exceeded',
    'High temperature detected',
    'The heat has exceeded the maximum advised bound.'
)