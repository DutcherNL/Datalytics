from datetime import timedelta

from datalytics.data_analysis.thresholds import FixedThreshold, LinearThreshold
from datalytics.settings_controller import settings

from .messages import AlertMessage


class Analyser:
    pass


class ShortTermAnalyser(Analyser):
    is_upper_threshold = True
    expire_time = timedelta(minutes=90)

    # Logging data
    name = None

    def __init__(self, threshold=None):
        self.threshold = threshold
        self.active_message = None

    def update(self, value, timestamp, room):
        """ Process an update of a new measurement """
        # Check that the last update was not too long ago
        self.check_expires(timestamp)

        if self.check(value):
            self._trigger_alert(value, timestamp, room)
        elif self.active_message:
            self._deactivate_trigger()

    def check(self, value):
        if self.is_upper_threshold and value >= self.threshold.get_threshold_value():
            return True
        elif not self.is_upper_threshold and value <= self.threshold.get_threshold_value():
            return True
        return False

    def _trigger_alert(self, value, timestamp, room):
        if self.active_message is None:
            # Set issue as active, create new alert
            self.active_message = AlertMessage(
                code=self.code,
                room = room,
                dt_start = timestamp,
                dt_last_update = timestamp,
                avg_value=value,
            )
            settings.load('storage').interface.messages.add(
                self.active_message
            )
        else:
            # update the timestamp and value
            self.active_message.update_avg(value, timestamp)
            settings.load('storage').interface.messages.update(
                self.active_message
            )

    def _deactivate_trigger(self):
        self.active_message.is_active = False
        settings.load('storage').interface.messages.update(
            self.active_message
        )
        self.active_message = None

    def check_expires(self, timestamp):
        """ Called when loading i.e. system downtime or after really long updates to ensure that gaps are not
        unneccessarily attributed to an alert. """
        if self.active_message:
            if timestamp - self.active_message.dt_last_update > self.expire_time:
                self._deactivate_trigger()


class UpperIndoorTemperatureAnalyser(ShortTermAnalyser):
    name = "Upper Temperature Limit Indoor"
    code = "Testcode-upper"
    user_message_active = "Exceed 26°"
    user_message_complete = "Exceed {value}° for {duration}"

    def __init__(self):
        super(UpperIndoorTemperatureAnalyser, self).__init__(FixedThreshold(26))


class LowerIndoorTemperatureAnalyser(ShortTermAnalyser):
    name = "Lower Temperature Limit Indoor"
    code = "Testcode-lower"
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

