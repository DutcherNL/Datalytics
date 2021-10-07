

class TupleDataUnpacker:
    """ Unpacks the measurement data assuming its a tuple with (datetime, value) """

    def unpack(self, measurement_data):
        return measurement_data[1], measurement_data[0]
