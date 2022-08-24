import datetime
from datalytics.analysis.analysers import *
from datalytics.settings_controller import settings
import warnings


sensor_types = {
    'TEMP': {
        'local_analysers': [UpperIndoorTemperatureAnalyser, LowerIndoorTemperatureAnalyser],
        'unit': "degrees Celsius"
    },
    'HUMID': {
        'local_analysers': [LowerIndoorRHAnalyser, UpperIndoorRHAnalyser],
        'unit': "relative humidity"
    },
    'CO2': {
        'local_analysers': [LowerIndoorCO2Analyser, UpperIndoorCO2Analyser],
        'unit': 'ppm'
    },
    'ILLUM': {
        'local_analysers': [],
        'unit': 'lux'
    },
}


class InvalidSensorType(KeyError):
    """ An exception declaring invalid sensor type """

    def __init__(self, sensor_type):
        self.type = type
        message = f"Sensor type {sensor_type} is not defined. Be sure this sensor is any of the following types:" \
                  f"{list(sensor_types.keys())} otherwise it will not work."
        super(InvalidSensorType, self).__init__(message)


class Sensor:
    """
    A sensor is an input for any sensor data coming in. Whenever a new value is detected, use update to update the sensor
    This triggers any local analysers as well as update the latest measured value on the storage (if applicable)

    """
    sensor_type = None
    last_update = None
    last_value = None

    def __init__(self, type, add_analysers=None):
        add_analysers = add_analysers or []

        if type not in sensor_types.keys():
            raise InvalidSensorType(type)
        self.sensor_type = type

        # Create the analysers
        self.analysers = []
        for analyser_class in sensor_types[self.sensor_type]['local_analysers']:
            self.analysers.append(analyser_class())
        for analyser_class in add_analysers:
            if isinstance(analyser_class, type):
                # object is class and not initialised
                self.analysers.append(analyser_class())
            else:
                # object was already initialised
                self.analysers.append(analyser_class)

    def update(self, value, timestamp, room, force_analysis=False):
        """
        Update the sensor with a new value and analyse it
        :param value:
        :param timestamp: The current timestamp, leave empty to use system datetime
        :param force_check: Whether the check needs to be run. This can lead to undesired results
        :return:
        """
        timestamp = timestamp or datetime.datetime.now()
        if self.last_update is not None and timestamp < self.last_update:
            if force_analysis:
                self.check_analysers(timestamp, value, room)
            else:
                warnings.warn(
                    "Measurement value was older than the latest update and shall not be processed. \n"
                    "Enable force_update on the update action to force analysis anyway",
                )
        else:
            self.check_analysers(timestamp, value, room)
            self._set_latest_value(value, timestamp, room)

    def _set_latest_value(self, value, timestamp, room):
        """
         Store the latest value recorded (does not check for timestamp)
        :param value: The latest value
        :param timestamp: The timestamp
        :return:
        """
        settings.load('storage').interface.measurements.update(
            value=value,
            room=room,
            sensor=self,
            timestamp=timestamp,
        )
        self.last_update = timestamp
        self.last_value = value

    def check_analysers(self, timestamp, value, room):
        """ Run the analysers to check for any potential errors """
        for analyser in self.analysers:
            analyser.update(timestamp=timestamp, value=value, room=room)
