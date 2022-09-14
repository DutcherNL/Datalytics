


""" Interfaces for connecting with the storage set-ups of important data """


class MessageStorageInterface:
    def add(self, message):
        """ Adds a alertive message """

    def update(self, message):
        """ Updates an alertive message """

    def load_active_messages(self):
        """ Loads and returns all rooms """


class RoomStorageInterface:
    def add(self, room):
        """ Adds a room """

    def update(self, room):
        """ Updates a room """

    def load_all(self):
        """ Loads and returns all rooms """


class MeasurementStorageInterface:
    def add(self, measurement):
        """ Adds a measurement """

    def update(self, measurement):
        """ Updates a measurement """

    def load_for_room(self, room):
        """ Loads and returns all measurements for a given room """


class StorageInterface:
    messages = None
    rooms = None
    measurements = None


interface = StorageInterface()