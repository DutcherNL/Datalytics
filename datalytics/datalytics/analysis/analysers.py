from datetime import timedelta

from datalytics.data_analysis.thresholds import FixedThreshold, LinearThreshold
from datalytics.settings_controller import settings

from .messages import AlertMessage


class Analyser:
    pass


class ShortTermAnalyser(Analyser):
    threshold = None
    expire_time = timedelta(minutes=90)

    # Logging data
    name = None

    def __init__(self, threshold=None):
        self.threshold = threshold or self.threshold
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


class UpperThresholdAnalyser(ShortTermAnalyser):
    def check(self, value):
        if value >= self.threshold.get_threshold_value():
            return True
        return False


class LowerThresholdAnalyser(ShortTermAnalyser):
    def check(self, value):
        if value <= self.threshold.get_threshold_value():
            return True
        return False


class UpperIndoorTemperatureAnalyser(UpperThresholdAnalyser):
    code = "heat_upperlimit_exceeded"
    threshold = FixedThreshold(26)


class LowerIndoorTemperatureAnalyser(LowerThresholdAnalyser):
    code = "heat_lowerlimit_exceeded"
    threshold = FixedThreshold(16)


class HumphreyTemperatureAnalyser(UpperThresholdAnalyser):
    code = "heat_upperlimit_humphrey_exceeded"

    def __init__(self, external_temperature_data_storage):
        super(HumphreyTemperatureAnalyser, self).__init__()
        self.threshold = LinearThreshold(
            data_storage=external_temperature_data_storage,
        )
        self.threshold.a = 0.53
        self.threshold.b = 13.8


class UpperIndoorRHAnalyser(UpperThresholdAnalyser):
    code = "rh_upperlimit_exceeded"
    threshold = FixedThreshold(60)


class LowerIndoorRHAnalyser(LowerThresholdAnalyser):
    code = "rh_lowerlimit_exceeded"
    threshold = FixedThreshold(25)


class UpperIndoorCO2Analyser(UpperThresholdAnalyser):
    code = "co2_baselimit_exceeded"
    threshold = FixedThreshold(1000)


class LowerIndoorCO2Analyser(UpperThresholdAnalyser):
    code = "co2_dangerlimit_exceeded"
    threshold = FixedThreshold(5000)


class LowIndoorLuxAnalyser(LowerThresholdAnalyser):
    code = "lux_minlimit_exceeded"
    threshold = FixedThreshold(100)


class HighIndoorLuxAnalyser(LowerThresholdAnalyser):
    code = "lux_minlimit_exceeded"
    threshold = FixedThreshold(500)