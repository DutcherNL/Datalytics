from . import TestCase
from time import sleep
from datetime import datetime

from datalytics.interface import AnalyserFront

analyser = AnalyserFront()


class LongTermTestCase(TestCase):
    data_type = None
    room_type = 'BASIC'

    def __init__(self):
        # Import a bit of delay to prevent errors in the database during testing
        sleep(1)

        self.room_name = f'test_{self.__class__.__name__}_{datetime.now().timestamp()}'
        self.room = analyser.add_room(room_type=self.room_type, name=self.room_name)
        super(LongTermTestCase, self).__init__()

    def _check_data(self, data, date_format='%d/%m/%y %H:%M:%S'):
        for data_entry in data:
            dt = datetime.strptime(data_entry[1], date_format)
            self.room.update_sensor(self.data_type, data_entry[0], dt)

            # print(self.room.sensors[self.data_type].has_active_analyser())
            self.assertEqual(
                data_entry[2],
                self.room.sensors[self.data_type].has_active_analyser(),
                msg=f"Entry at {dt} is not correct"
            )


class LongTermTempTestCase(LongTermTestCase):
    data_type = 'TEMP'

    def test_low_data(self):
        data = [
            (20, "22/05/10 11:00:00", False),
            (19, "22/05/10 11:05:00", False),
            (18, "22/05/10 11:10:00", False),
            (18, "22/05/10 11:15:00", False),
            (15, "22/05/10 11:20:00", True),
            (17, "22/05/10 11:25:00", False),
            (17, "22/05/10 11:30:00", False),
            (17, "22/05/10 11:35:00", False),
            (18, "22/05/10 11:40:00", False),
            (17, "22/05/10 11:45:00", False),
            (16, "22/05/10 11:50:00", True),
            (16, "22/05/10 11:55:00", True),
            (15, "22/05/10 12:00:00", True),
            (14, "22/05/10 12:05:00", True),
            (13, "22/05/10 12:10:00", True),
            (14, "22/05/10 12:15:00", True),
            (15, "22/05/10 12:20:00", True),
            (17, "22/05/10 12:25:00", False),
            (18, "22/05/10 12:30:00", False),
            (19, "22/05/10 12:35:00", False),
        ]
        self._check_data(data)

    def test_high_data(self):
        data = [
            (20, "29/05/10 13:00:00", False),
            (22, "29/05/10 13:05:00", False),
            (24, "29/05/10 13:10:00", False),
            (25, "29/05/10 13:15:00", False),
            (27, "29/05/10 13:20:00", True),
            (25, "29/05/10 13:25:00", False),
            (24, "29/05/10 13:30:00", False),
            (19, "29/05/10 13:35:00", False),
            (20, "29/05/10 13:40:00", False),
            (20, "29/05/10 13:45:00", False),
            (27, "29/05/10 13:50:00", True),
            (28, "29/05/10 13:55:00", True),
            (28, "29/05/10 14:00:00", True),
            (29, "29/05/10 14:05:00", True),
            (30, "29/05/10 14:10:00", True),
            (27, "29/05/10 14:15:00", True),
            (26, "29/05/10 14:20:00", True),
            (25, "29/05/10 14:25:00", False),
            (24, "29/05/10 14:30:00", False),
            (20, "29/05/10 14:35:00", False),
        ]
        self._check_data(data)



class LongTermHumidTestCase(LongTermTestCase):
    data_type = 'HUMID'

    def test_low_data(self):
        data = [
            (30, "22/05/10 11:00:00", False),
            (29, "22/05/10 11:05:00", False),
            (28, "22/05/10 11:10:00", False),
            (27, "22/05/10 11:15:00", False),
            (25, "22/05/10 11:20:00", True),
            (26, "22/05/10 11:25:00", False),
            (27, "22/05/10 11:30:00", False),
            (28, "22/05/10 11:35:00", False),
            (29, "22/05/10 11:40:00", False),
            (30, "22/05/10 11:45:00", False),
            (24, "22/05/10 11:50:00", True),
            (23, "22/05/10 11:55:00", True),
            (25, "22/05/10 12:00:00", True),
            (24, "22/05/10 12:05:00", True),
            (23, "22/05/10 12:10:00", True),
            (24, "22/05/10 12:15:00", True),
            (25, "22/05/10 12:20:00", True),
            (27, "22/05/10 12:25:00", False),
            (28, "22/05/10 12:30:00", False),
            (29, "22/05/10 12:35:00", False),
        ]
        self._check_data(data)

    def test_high_data(self):
        data = [
            (50, "29/05/10 13:00:00", False),
            (52, "29/05/10 13:05:00", False),
            (54, "29/05/10 13:10:00", False),
            (58, "29/05/10 13:15:00", False),
            (61, "29/05/10 13:20:00", True),
            (58, "29/05/10 13:25:00", False),
            (54, "29/05/10 13:30:00", False),
            (59, "29/05/10 13:35:00", False),
            (59, "29/05/10 13:40:00", False),
            (58, "29/05/10 13:45:00", False),
            (61, "29/05/10 13:50:00", True),
            (63, "29/05/10 13:55:00", True),
            (64, "29/05/10 14:00:00", True),
            (67, "29/05/10 14:05:00", True),
            (68, "29/05/10 14:10:00", True),
            (65, "29/05/10 14:15:00", True),
            (64, "29/05/10 14:20:00", True),
            (59, "29/05/10 14:25:00", False),
            (58, "29/05/10 14:30:00", False),
            (56, "29/05/10 14:35:00", False),
        ]
        self._check_data(data)


class LongTermCO2TestCase(LongTermTestCase):
    data_type = 'CO2'

    def test_low_data(self):
        data = [
            (910, "22/05/10 18:00:00", False),
            (930, "22/05/10 18:05:00", False),
            (950, "22/05/10 18:10:00", False),
            (970, "22/05/10 18:15:00", False),
            (1010, "22/05/10 18:20:00", True),
            (990, "22/05/10 18:25:00", False),
            (980, "22/05/10 18:30:00", False),
            (970, "22/05/10 18:35:00", False),
            (915, "22/05/10 18:40:00", False),
            (110, "22/05/10 18:45:00", False),
            (1110, "22/05/10 18:50:00", True),
            (1035, "22/05/10 18:55:00", True),
            (1040, "22/05/10 19:00:00", True),
            (1080, "22/05/10 19:05:00", True),
            (1110, "22/05/10 19:10:00", True),
            (1080, "22/05/10 19:15:00", True),
            (1050, "22/05/10 19:20:00", True),
            (990, "22/05/10 19:25:00", False),
            (985, "22/05/10 19:30:00", False),
            (965, "22/05/10 19:35:00", False),
        ]
        self._check_data(data)

    def test_high_data(self):
        # High data can not be tested through the designed approach as it also triggers on 4000 on the other analyser
        pass


class LongTermLuxTestCase(LongTermTestCase):
    data_type = 'ILLUM'
    room_type = 'WORK'

    def test_high_data(self):
        data = [
            (510, "22/05/10 18:00:00", False),
            (530, "22/05/10 18:05:00", False),
            (550, "22/05/10 18:10:00", False),
            (510, "22/05/10 18:15:00", False),
            (490, "22/05/10 18:20:00", True),
            (515, "22/05/10 18:25:00", False),
            (553, "22/05/10 18:30:00", False),
            (578, "22/05/10 18:35:00", False),
            (569, "22/05/10 18:40:00", False),
            (532, "22/05/10 18:45:00", False),
            (495, "22/05/10 18:50:00", True),
            (467, "22/05/10 18:55:00", True),
            (485, "22/05/10 19:00:00", True),
            (421, "22/05/10 19:05:00", True),
            (410, "22/05/10 19:10:00", True),
            (380, "22/05/10 19:15:00", True),
            (350, "22/05/10 19:20:00", True),
            (650, "22/05/10 19:25:00", False),
            (685, "22/05/10 19:30:00", False),
            (665, "22/05/10 19:35:00", False),
        ]
        self._check_data(data)

    def test_high_data(self):
        # Low data can not be tested specifically as it also triggers the below 500 threshold
        pass