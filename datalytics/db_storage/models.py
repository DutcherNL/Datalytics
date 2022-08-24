from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Float, Boolean
from sqlalchemy.schema import ForeignKey

from datalytics.settings_controller import settings

class SQLTable:

    def __init__(self, meta):
        self.table = Table(self.table_name, meta, *self.columns)

    def _execute(self, command, engine=None, has_return=False):
        if engine is None:
            # Set a default engine if it is not passed
            engine = settings.load('storage').interface.db_engine

        conn = engine.connect()
        conn.execute(command)
        conn.close()

    def _select(self, filter=None, engine=None):
        filter = filter or {}
        if engine is None:
            # Set a default engine if it is not passed
            engine = settings.load('storage').interface.db_engine

        conn = engine.connect()
        result = conn.execute(self.table.select().where(*filter))

        # Translate the list to a processable format as we will close the connection afterwards
        results = []
        for row in result:
            results.append(dict(row))

        conn.close()
        return results


class MessageTable(SQLTable):
    table_name = 'messages'
    columns = [
        Column('id', Integer, primary_key = True),
        Column('code', String),
        Column('room_id', Integer),
        Column('dt_start', DateTime),
        Column('dt_last_update', DateTime),
        Column('avg_value', Float),
        Column('is_active', Boolean),
    ]

    def insert(self, message, engine=None):
        insert_command = self.table.insert().values(
            code = message.code,
            room_id = message.room.id,
            dt_start= message.dt_start,
            dt_last_update = message.dt_last_update,
            avg_value = message.avg_value,
            is_active = message.is_active,
        )
        self._execute(insert_command, engine)

        # Get the id, this can not be done through returning() due to limitations of sqlalchemy and sqlite
        # So we retrieve the instance instead through other attributes
        result = self._select(filter=[
            self.table.c.room_id == message.room.id,
            self.table.c.code == message.code,
            self.table.c.dt_start == message.dt_start,
        ])
        message.id = result[0]['id']

    def update(self, message, engine=None):
        msg_update = self.table.update().\
            where(self.table.c.id==message.id).\
            values(
            dt_last_update = message.dt_last_update,
            avg_value = message.avg_value,
            is_active = message.is_active
        )
        self._execute(msg_update, engine)

    def select_active_messages(self, room, engine):
        """ Returns all active messages. Used as program start-up """
        return self._select(filter=[
            self.table.c.is_active == True,
            self.table.c.room_id == room.id,
        ], engine=engine)



class RoomTable(SQLTable):
    table_name = 'rooms'
    columns = [
        Column('id', Integer, primary_key = True),
        Column('name', String),
        Column('type', String(length=5)),
    ]

    def insert(self, room, engine=None):
        insert_command = self.table.insert().values(
            id = room.id,
            name = room.name,
            type = room.room_type,
        )
        self._execute(insert_command, engine)

    def update(self, room, engine=None):
        msg_update = self.table.update(). \
            where(self.table.c.id==room.id). \
            values(
            name=room.name
        )
        self._execute(msg_update, engine)

    def select_all(self, engine=None):
        return self._select(engine=engine)


class MeasurementTable(SQLTable):
    table_name = 'room_measurement'
    columns = [
        Column('id', Integer, primary_key = True),
        Column('value', Float),
        Column('dt_last_update', DateTime),
        Column('type', String(length=4)),
        Column('room_id', ForeignKey("rooms.id")),
        Column('danger_level', Integer)
    ]

    def insert(self, value, sensor, room, timestamp=None, engine=None):
        insert_command = self.table.insert().values(
            value=value,
            type=sensor.sensor_type,
            room_id=room.id,
            dt_last_update=timestamp
        )
        self._execute(insert_command, engine)

    def update(self, value, room, sensor, timestamp, engine=None):
        msg_update = self.table.update(). \
            filter_by(room_id=room.id, type=sensor.sensor_type). \
            values(
            value=value,
            dt_last_update=timestamp,
        )
        self._execute(msg_update, engine)

    def select_for_room(self, room, engine=None):
        """ Returns measurement value entries for a given room """
        return self._select(filter=[self.table.c.room_id == room.id], engine=engine)




