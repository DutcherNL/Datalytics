



class DataStorage:
    storage = None
    update_informers = None

    def __init__(self, name=None):
        self.name = name
        self.storage = []
        self.update_informers = {}

    def append(self, y_value, x_value=None):
        if x_value is None:
            x_value = len(self.storage)

        new_value = (x_value, y_value)
        self.storage.append(new_value)
        self._trigger_update(new_value)

    def get_latest_value(self):
        if self.storage.__len__() > 0:
            return self.storage[self.storage.__len__()-1]
        return 0, 0

    def _trigger_update(self, updated_value):
        """ Update all hooks connected """
        for key, connection in self.update_informers.items():
            connection(updated_value)

    def __getitem__(self, item):
        assert isinstance(item, int)
        return self.storage[item]

    @property
    def min_y_value(self):
        return -10

    @property
    def max_y_value(self):
        return 40

    def get_x_values(self, n_last=None):
        if n_last is not None and n_last < self.storage.__len__():
            return [i[0] for i in self.storage[self.storage.__len__()-n_last:]]
        return [i[0] for i in self.storage]

    def get_y_values(self, n_last=None):
        if n_last is not None and n_last < self.storage.__len__():
            return [i[1] for i in self.storage[self.storage.__len__()-n_last:]]
        return [i[1] for i in self.storage]

    def on_update(self, function, name=None):
        if name is None:
            name = str(function.__name__)
        self.update_informers[name] = function


class TransformedDataStorage:

    def __init__(self, data_storage:DataStorage, transformation):
        self.data_storage = data_storage
        self.transformation = transformation

    def __getattr__(self, item):
        return getattr(self.data_storage, item)

    def get_y_values(self, n_last:int=None):
        return [self.transformation(value) for value in self.data_storage.get_y_values(n_last)]

