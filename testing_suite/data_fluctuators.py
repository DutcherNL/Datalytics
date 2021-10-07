import time, threading, math

class CosineFluctuator:
    refresh_speed = 0.05
    amplitude = 1
    increment_step = 0.1

    def __init__(self, data_storage_obj, amplitude=None, increment_step=None):
        self.data_storage_obj = data_storage_obj
        self.amplitude = amplitude if amplitude is not None else self.amplitude
        self.increment_step = increment_step or self.increment_step

        self.last_computed_value = 0
        self.ticks = 0
        self.call_loop()

    def call_loop(self):
        self.fluctuate()
        threading.Timer(self.refresh_speed, self.call_loop).start()


    def fluctuate(self):
        value = self.data_storage_obj.get_latest_value()[1]

        new_increment = self.compute_fluctuation()
        value += new_increment - self.last_computed_value

        self.last_computed_value = new_increment
        self.data_storage_obj.append(value)

    def compute_fluctuation(self):
        value = self.amplitude * math.cos(self.ticks)
        self.ticks += self.increment_step
        return value

