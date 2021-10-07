from datalytics.datalytics.data_storage.models import ShortTermAnalyser, IndoorTemperatureAnalyser, HumphreyTemperatureAnalyser
from datalytics.datalytics.data_storage.data_unpackers import TupleDataUnpacker


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


class TempDataAnalyser(DataAnalyseInterface):
    unpacker_class = TupleDataUnpacker
    analysis_classes = [IndoorTemperatureAnalyser, HumphreyTemperatureAnalyser]

    def __init__(self, external_temperature_data=None, **kwargs):
        super(TempDataAnalyser, self).__init__(**kwargs)

        self.data_analysers = [
            IndoorTemperatureAnalyser(),
            HumphreyTemperatureAnalyser(external_temperature_data),
        ]