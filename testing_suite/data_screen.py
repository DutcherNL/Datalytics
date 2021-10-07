import math
from PySide2.QtCore import Qt, QSize, QTimer
from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedLayout, QPushButton
from PySide2.QtGui import QPalette, QColor

from testing_suite.charts import DataGraph


class TestWindow(QMainWindow):
    def __init__(self, window_name, data_storage):
        super().__init__()

        self.setWindowTitle(window_name)
        self.setMinimumSize(QSize(400, 300))


        layout = QVBoxLayout()

        if isinstance(data_storage, list):
            for data_storage_obj in data_storage:
                layout.addWidget(DataGraph(data_storage_obj))
        else:
            layout.addWidget(DataGraph(data_storage))

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

