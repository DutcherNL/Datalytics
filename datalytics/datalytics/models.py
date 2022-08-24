from .sensors import Sensor
from .analysis import analysers

""" Define the various room types. Some room types may have different requirements or triggers """
room_types = {
    'BASIC': {
        'readable': 'Neutral room',
    },
    'BATH': {
        'readable': 'Bath room',
        'local_analysers': {
            'TEMP': []
        }
    },
    'WORK': {
        'readable': 'Work room',
        'local_analysers': {
            'ILLUM': [
                analysers.LowIndoorLuxAnalyser,
                analysers.HighIndoorLuxAnalyser,
            ]
        }
    },
    'BED': {
        'readable': 'Bedroom',
    },
}


class Room:
    """ Defines a room in which measurement equipment is connected """
    name = None
    room_type = None

    sensors = None

    def __init__(self, room_type, name, initial_sensor_types=None):
        initial_sensor_types = initial_sensor_types or []
        self.room_type = room_type
        self.name = name
        self.sensors = []
        if room_type not in room_types.keys():
            raise KeyError(f"Room type {type} is not defined. Be sure this sensor is any of the following types:"
                           f"{room_types.keys()} otherwise it will not work.")

        self.sensors = {}
        for sensor_type in initial_sensor_types:
            self.add_sensor(sensor_type)


    def add_sensor(self, sensor_type):
        """ Adds a sensor of the given type to the room """
        if sensor_type in self.sensors.keys():
                raise KeyError("A sensor with the given parameters was already defined for this room")

        add_analysers = room_types[self.room_type].get('local_analysers', {}).get(sensor_type, None)
        self.sensors[sensor_type] = Sensor(sensor_type, add_analysers=add_analysers)
        return self.sensors[sensor_type]

    def update_sensor(self, sensor_type, value, timestamp, force_analysis=False):
        """
        Update the room sensor of the given sensor type
        :param sensor_type: The defined sensor type
        :param value: The measured value
        :param timestamp: The timestamp of the measurement
        :param force_analysis: Whether the analysis needs to be executed even if it contains an older timestamp
        :return:
        """
        try:
            self.sensors[sensor_type].update(value, timestamp, self, force_analysis=force_analysis)
        except KeyError:
            self.add_sensor(sensor_type=sensor_type)
            self.sensors[sensor_type].update(value, timestamp, self, force_analysis=force_analysis)