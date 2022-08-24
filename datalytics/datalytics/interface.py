from datalytics.data_analysis.models import ShortTermAnalyser, IndoorTemperatureAnalyser, HumphreyTemperatureAnalyser
from datalytics.data_analysis.data_unpackers import TupleDataUnpacker

from datalytics.settings_controller import settings

from datalytics.models import Room

class DataAnalyseInterface:
    unpacker_class = None

    def __init__(self, data_unpacker: TupleDataUnpacker=None, data_analyser:ShortTermAnalyser=None):
        self.data_unpacker = data_unpacker or self.unpacker_class()
        self.data_analysers = data_analyser


    def inform_real_time(self, measurement_data):
        if isinstance(self.data_analysers, list):
            analysers = self.data_analysers
        else:
            analysers = [self.data_analysers]

        unpacked_data = self.data_unpacker.unpack(measurement_data)

        for analyser in analysers:
            analyser.update(*unpacked_data)


class AnalyserFront:

    rooms = None
    highest_id = 0

    def __init__(self):
        self.rooms = {}

        # prep storage
        self.storage = settings.load('storage').interface
        self._load_rooms()

    def _load_rooms(self):
        for room in self.storage.rooms.load_all():
            self.highest_id = max(self.highest_id, room.id)
            self.rooms[str(room.id)] = room

            # Load in the measurement values
            measurements = self.storage.measurements.load_for_room(room)
            for m in measurements:
                try:
                    sensor = room.add_sensor(m['type'])
                except KeyError:
                    # Duplicates encountered, for some reason. So take that into account.
                    print(f"Duplicate measurement data has been detected on the server on {room.name} - {m['type']}")
                    sensor = room.sensors[m['type']]
                    if m['timestamp'] > sensor.last_update:
                        sensor.last_update = m['timestamp']
                        sensor.last_value = m['value']
                else:
                    sensor.last_update = m['timestamp']
                    sensor.last_value = m['value']
            # Load active messages and set them to the relevant analysers
            msg_dict = {}
            for msg in self.storage.messages.load_active_messages(room):
                msg_dict[msg.code] = msg

            for sensor in room.sensors.values():
                for analyser in sensor.analysers:
                    if analyser.code in msg_dict.keys():
                        analyser.active_message = msg_dict.pop(analyser.code)
            for key in msg_dict.keys():
                print(f"Code {key} could not be attributed to the correct analyser upon launch.")


    def add_room(self, room_type, name, sensor_types=None):
        """
        Adds a room to the system
        :param room_type: The type of room
        :param name: The name of the room
        :param sensor_types: The types of sensors active in the room
        :return:
        """
        room = Room(room_type, name, initial_sensor_types=sensor_types)
        new_id = self.highest_id + 1
        room.id = new_id
        self.rooms[str(new_id)] = room

        self.storage.rooms.add(room)

    def get_room(self, name=None, room_id=None, fall_back_as_id=False) -> Room:
        """
        Returns the room with the given name or id
        :param name: The name of the room (room_id should be None)
        :param room_id: The id  of the room (name should  be None)
        :param fall_back_as_id: search id if name does not yield results
        :return: The room or None
        """
        assert not (name and room_id)
        assert name or room_id
        if name:
            for room in self.rooms.values():
                if room.name == name:
                    return room
            if fall_back_as_id:
                return self.rooms.get(str(name))
            return None
        else:
            return self.rooms.get(str(room_id))



class TempDataAnalyser(DataAnalyseInterface):
    unpacker_class = TupleDataUnpacker
    analysis_classes = [IndoorTemperatureAnalyser, HumphreyTemperatureAnalyser]

    def __init__(self, external_temperature_data=None, **kwargs):
        super(TempDataAnalyser, self).__init__(**kwargs)

        self.data_analysers = [
            IndoorTemperatureAnalyser(),
            HumphreyTemperatureAnalyser(external_temperature_data),
        ]