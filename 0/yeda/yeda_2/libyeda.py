import board
import time
import analogio
from ulab import numpy as np
from ulab import array as ary

class Yeda:

    def __init__(self, eda_pin = board.GP27_A1, interval = 0.1):
        self.eda_pin = eda_pin
        self.sensor = analogio.AnalogIn(eda_pin)
        self.interval = interval
        self.time, self.last_time = (None, None)
        self.value, self.last_value = (None,None)
        self.data = np.empty(0,3)
        self.events = np.empty(0,3)

    def result(self):
        return (self.time, self.value, self.delta)

    def update(self):
        this_time = time.monotonic()
        if self.interval > (this_time - self.last_time):
            self.time = this_time
            self.value = 65536 / self.sensor.value 
            self.delta = self.last_value - self.value
            return (True, self.result())
        else:
            return (False, self.result())

    def record(self):
        np.append(self.data, self.result(), axis=0)

    def record_event(self, label = "TOI", value = 1):
        this_time = time.monotonic()
        np.append(self.data, (this_time, str(label), float(value)), 
                  axis=0)

