



class Threshold:

    def get_threshold_value(self):
        raise NotImplementedError()


class FixedThreshold(Threshold):
    threshold_value = None

    def __init__(self, threshold_value):
        self.threshold_value = threshold_value

    def get_threshold_value(self):
        return self.threshold_value


class LinearThreshold(Threshold):
    a = 1
    b = 0

    def __init__(self, data_storage=None):
        self.data_storage = data_storage

    def get_threshold_value(self):
        ext_value = self.data_storage.get_latest_value()[1]
        value = self.a * ext_value + self.b
        return value