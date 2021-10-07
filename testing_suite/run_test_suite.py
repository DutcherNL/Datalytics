import sys

from PySide2.QtWidgets import QApplication

from testing_suite.data_screen import TestWindow
from testing_suite.data_storage import DataStorage, TransformedDataStorage
from testing_suite.data_fluctuators import CosineFluctuator

from datalytics import TempDataAnalyser

class TestingSetup:
    name = "General testing"

    def run(self):
        # Set the application
        app = QApplication(sys.argv)

        window = TestWindow(window_name=self.name, data_storage=self.data_storage)
        window.show()

        # Start the event loop.
        app.exec_()


class TestTempSetup(TestingSetup):
    name = 'Temperature testing'

    def __init__(self):
        self.data_storage = []

        data_storage_obj = DataStorage("Indoor temp")
        CosineFluctuator(data_storage_obj, amplitude=0)

        data_outdoor = DataStorage("Outdoor temp")
        CosineFluctuator(data_outdoor, amplitude=12)

        analyser = TempDataAnalyser(data_outdoor)
        data_storage_obj.on_update(analyser.inform_real_time)

        def transform(value):
            return 0.53 * value + 13.8

        upperT_limit_data_storage = TransformedDataStorage(data_outdoor, transform)


        self.data_storage.append({'main': data_storage_obj, 'top': upperT_limit_data_storage})
        self.data_storage.append({'main': data_outdoor})

        self.run()





temp_testing = TestTempSetup()