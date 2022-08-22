from datalytics.data_analysis.thresholds import FixedThreshold, LinearThreshold


class Analyser:
    pass


class ShortTermAnalyser(Analyser):
    is_upper_threshold = True

    # Logging data
    name = None
    user_message_active = None

    def __init__(self, threshold=None):
        self.threshold = threshold
        self.active_timestamp = None

    def update(self, value, timestamp, room):
        # print(f'{value} - {timestamp} | {self.threshold.get_threshold_value()}')
        if self.is_upper_threshold and value >= self.threshold.get_threshold_value():
            self._trigger_alert(value, timestamp)
        elif not self.is_upper_threshold and value <= self.threshold.get_threshold_value():
            self._trigger_alert(value, timestamp)
        elif self.active_timestamp:
            self._deactivate_trigger(timestamp)

    def _trigger_alert(self, value, timestamp):
        if self.active_timestamp is None:
            self.active_timestamp = timestamp
            print(self.user_message_active)

        # msg = self.user_message.format(
        #     # duration = datetime.timedelta()
        # )

    def _deactivate_trigger(self, timestamp):
        print(self.user_message_complete.format(
            value = self.threshold.get_threshold_value(),
            duration = timestamp - self.active_timestamp,
        ))
        self.active_timestamp = None


class UpperIndoorTemperatureAnalyser(ShortTermAnalyser):
    name = "Upper Temperature Limit Indoor"
    user_message_active = "Exceed 26°"
    user_message_complete = "Exceed {value}° for {duration}"

    def __init__(self):
        super(UpperIndoorTemperatureAnalyser, self).__init__(FixedThreshold(26))


class LowerIndoorTemperatureAnalyser(ShortTermAnalyser):
    name = "Lower Temperature Limit Indoor"
    user_message_active = "Exceed 16°"
    user_message_complete = "Exceed {value}° for {duration}"
    is_upper_threshold = False

    def __init__(self):
        super(LowerIndoorTemperatureAnalyser, self).__init__(FixedThreshold(16))


class HumphreyTemperatureAnalyser(ShortTermAnalyser):
    name = "Upper Temperature Limit Indoor"
    user_message_active = "Exceed XX°"
    user_message_complete = "Exceed {value}° for {duration}"

    def __init__(self, external_temperature_data_storage):
        super(HumphreyTemperatureAnalyser, self).__init__()
        self.threshold = LinearThreshold(
            data_storage=external_temperature_data_storage,
        )
        self.threshold.a = 0.53
        self.threshold.b = 13.8

