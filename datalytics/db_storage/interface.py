import warnings

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import IntegrityError

from .models import MessageTable


class DBStorageInterface:
    db_engine = None

    def __init__(self):
        self.setup()

    def setup(self):
        """
        Method run when link is set-up
        :return:
        """

        meta = MetaData()

        self.db_engine = create_engine("sqlite:///db.sqlite", echo=True)

        self.msg_table = MessageTable(meta)

        meta.create_all(self.db_engine)
        print("Setup has run")


    def breakdown(self):
        """
        Method run when needing to break down this link
        :return:
        """

    def add_message(self, message, fail_silently=False):
        try:
            self.msg_table.insert(message, self.db_engine)
        except IntegrityError:
            if not fail_silently:
                raise

    def update_message(self, message, create_if_nonexistent=False):
        if create_if_nonexistent:
            warnings.warn(f"{self.__class__.__name__} does not support creation for non-existent")

        self.msg_table.update(message, self.db_engine)



    def get_messages(self):
        pass


interface = DBStorageInterface()