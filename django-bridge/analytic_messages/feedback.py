


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

        self.texts[code] = data

    def get_readable(self, code, data_type):
        return self.texts.get(code, {}).get(data_type, '-NOT REGISTERED-')

    def get_registered_codes(self):
        return self.texts.keys()


data_info = CodeDataCommunication()


data_info.register(
    'test',
    'Test event',
    'This is a test event'
)

data_info.register(
    'heat_upperlimit_exceeded',
    'High temperature detected',
    'Temperature exceeds recommanded value.'
)

data_info.register(
    'heat_lowerlimit_exceeded',
    'Low temperature detected',
    'The temperature is lower than the recommended value.'
)

data_info.register(
    'rh_upperlimit_exceeded',
    'High humidity detected',
    'The relative humidity is higher than the recommended value.'
)

data_info.register(
    'rh_lowerlimit_exceeded',
    'Low humidity detected',
    'The relative humidity is lower than the recommended value.'
)

data_info.register(
    'rh_abs_lowerlimit_exceeded',
    'Low humidity detected',
    'The absolute humidity is lower than the recommended value.'
)

data_info.register(
    'co2_baselimit_exceeded',
    'High CO2 concentration detacted',
    'The CO2 concentration is higher than the recommended value.'
)

data_info.register(
    'co2_baselimit_exceeded',
    'Dangerously high CO2 concentration detacted',
    'The CO2 concentration is dangerously high. Ventilate the room now!.'
)

data_info.register(
    'lux_500limit_exceeded',
    'Non-ideal light instensity detected',
    'The illuminance level is lower than the recommanded value for a work environment',
)