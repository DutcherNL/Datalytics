import warnings
from datetime import datetime

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import IntegrityError

from .models import MessageTable, RoomTable, MeasurementTable
from datalytics.storage import MessageStorageInterface, RoomStorageInterface, MeasurementStorageInterface
from datalytics.settings_controller import settings
from datalytics.models import Room
from datalytics.analysis.messages import AlertMessage


class DBStorageMessageInterface(MessageStorageInterface):
    def __init__(self, db_engine, metadata):
        self.db_engine = db_engine
        self.msg_table = MessageTable(metadata)

    def add(self, message, fail_silently=False):
        """ Adds a alertive message """
        try:
            self.msg_table.insert(message, self.db_engine)
        except IntegrityError:
            if not fail_silently:
                raise

    def update(self, message):
        """ Updates an alertive message """
        self.msg_table.update(message, self.db_engine)

    def load_active_messages(self, room):
        """ Returns active messages of a room """
        msg_list = []
        for msg in self.msg_table.select_active_messages(room, self.db_engine):
            message = AlertMessage(
                code = msg['code'],
                room = room,
                dt_start = msg['dt_start'],
                dt_last_update = msg['dt_last_update'],
                avg_value = float(msg['avg_value']),
                id = msg['id'],
            )
            msg_list.append(
                message
            )
        return msg_list


class DBStorageMeasurementInterface(MeasurementStorageInterface):
    def __init__(self, db_engine, metadata):
        self.db_engine = db_engine
        self.measurement_table = MeasurementTable(metadata)

    def update(self, value, room, sensor, timestamp):
        """ Updates an alertive message """
        if sensor.last_update:
            method = 'update'
        else:
            # There is no update executed. So there is no value stored
            method = 'insert'

        self.measurement_table.__getattribute__(method)(
            value=value,
            room=room,
            sensor=sensor,
            timestamp=timestamp,
            engine=self.db_engine
        )

    def load_for_room(self, room):
        measurements = self.measurement_table.select_for_room(room, engine=self.db_engine)
        for m in measurements:
            m['timestamp'] = m['dt_last_update']
        return measurements


class DBStorageRoomInterface(RoomStorageInterface):
    def __init__(self, db_engine, metadata):
        self.db_engine = db_engine
        self.room_table = RoomTable(metadata)

    def add(self, room, fail_silently=True):
        """ Adds a alertive message """
        try:
            self.room_table.insert(room, self.db_engine)
        except IntegrityError:
            if not fail_silently:
                raise

    def update(self, message, create_if_nonexistent=False):
        """ Updates an alertive message """
        if create_if_nonexistent:
            warnings.warn(f"{self.__class__.__name__} does not support creation for non-existent")

        self.room_table.update(message, self.db_engine)

    def load_all(self):
        rooms = []
        for room_data in self.room_table.select_all():
            room = Room(
                room_type=room_data['type'],
                name=room_data['name'],
            )
            room.id = room_data['id']
            rooms.append(room)

        return rooms


class DBStorageInterface:
    def __init__(self):
        meta = MetaData()

        self.db_engine = create_engine(f"sqlite:///{settings.db_name}", echo=False)
        self.messages = DBStorageMessageInterface(db_engine=self.db_engine, metadata=meta)
        self.rooms = DBStorageRoomInterface(db_engine=self.db_engine, metadata=meta)
        self.measurements = DBStorageMeasurementInterface(db_engine=self.db_engine, metadata=meta)

        meta.create_all(self.db_engine)

    def breakdown(self):
        """
        Method run when needing to break down this link
        :return:
        """

interface = DBStorageInterface()