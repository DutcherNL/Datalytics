from datalytics.datalytics.data_storage.thresholds import FixedThreshold, LinearThreshold




class ShortTermAnalyser:
    is_upper_threshold = True

    # Logging data
    name = None
    user_message_active = None

    def __init__(self, threshold=None):
        self.threshold = threshold
        self.active_timestamp = None

    def update(self, value, timestamp):
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


class IndoorTemperatureAnalyser(ShortTermAnalyser):
    name = "Upper Temperature Limit Indoor"
    user_message_active = "Exceed 26°"
    user_message_complete = "Exceed {value}° for {duration}"

    def __init__(self):
        super(IndoorTemperatureAnalyser, self).__init__(FixedThreshold(26))


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

