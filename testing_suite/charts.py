from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLayout, QSlider, QPushButton
from PySide2.QtGui import QPalette, QColor
from pyqtgraph.widgets.PlotWidget import PlotWidget
from pyqtgraph.functions import mkPen

from testing_suite.data_storage import DataStorage

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

        self.setMinimumWidth(100)


class DataGraph(QWidget):

    def __init__(self, data:dict):
        super(DataGraph, self).__init__()

        self.chart_data = data

        main_layout = QHBoxLayout()
        main_layout.addWidget(TestPlotWidget(self.chart_data))

        self.slider = QSlider()
        self.slider.setMinimum(self.chart_data['main'].min_y_value)
        self.slider.setMaximum(self.chart_data['main'].max_y_value)
        self.slider.setSingleStep(1)
        self.slider.sliderReleased.connect(self.add_new_measurement)

        button = QPushButton("Add new value")
        button.clicked.connect(self.add_new_measurement)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.slider)
        button_layout.addWidget(button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def add_new_measurement(self):
        storage = self.chart_data['main'].storage
        storage[len(storage)-1] = (storage[len(storage)-1][0], self.slider.value())

        # self.chart_data['main'].storage[]
        # self.chart_data['main'].append(self.slider.value())



class TestPlotWidget(PlotWidget):

    def __init__(self, chart_data: dict):
        super(TestPlotWidget, self).__init__()
        self.chart_data = chart_data
        self.chart_data['main'].on_update(self.on_data_update)

        self.setBackground('w')
        self.setTitle(chart_data['main'].name, color="#000000", size="12pt")
        styles = {"color": "#000", "font-size": "20px"}
        self.setLabel("left", "Temperature (°C)", **styles)

        self.other_lines = {}
        for datakey in chart_data.keys():
            if datakey == 'main':
                self.measurement_data_line = self.plot([0,1,],[0,1,], name="", pen=mkPen(color='#000'))
            else:
                self.other_lines[datakey] = self.plot([0,1,],[0,1,], datakey, pen=mkPen(color='#f00'))


        self.show()

    def on_data_update(self, measurement_data):
        self.show()

    def show(self):
        self.setYRange(self.chart_data['main'].min_y_value, self.chart_data['main'].max_y_value, padding=0)

        n_last = 10

        self.measurement_data_line.setData(
            self.chart_data['main'].get_x_values(n_last),
            self.chart_data['main'].get_y_values(n_last),
        )
        for key, line in self.other_lines.items():
            line.setData(
                self.chart_data[key].get_x_values(n_last),
                self.chart_data[key].get_y_values(n_last)
            )

