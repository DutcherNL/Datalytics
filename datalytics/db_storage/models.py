from sqlalchemy import Table, Column, Integer, String







class MessageTable:
    table_name = 'messages'
    columns = [
        Column('id', Integer, primary_key = True),
        Column('code', String),
        Column('duration', String),
        Column('avg_value', String),
    ]


    def __init__(self, meta):
        self.table = Table(self.table_name, meta, *self.columns)

    def insert(self, message, engine):
        insert_command = self.table.insert().values(
            id = message.id,
            code = message.code,
            **message.message_vars
        )
        conn = engine.connect()
        conn.execute(insert_command)
        conn.close()

    def update(self, message, engine):
        msg_update = self.table.update().\
            where(self.table.c.id==message.id).\
            values(
            **message.message_vars
        )

        conn = engine.connect()
        conn.execute(msg_update)
        conn.close()



