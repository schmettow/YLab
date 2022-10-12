import board
import time
import analogio
from ulab import numpy as np
from ulab import array as ary

class Yeda:
    n_instances = int(0)

    def __init__(self,  pin = board.GP27_A1, 
                        update_interval = 0.1, 
                        save_interval = 10):
        """
        Creates a new YEDA sensor object

        :param eda_pin: IO port YEDA is connected to, default is Grove slot 
        :param update_interval float: time between measures
        :param save_interval float: time between pushing the collected data to a file
        :return: None
        :rtype: NoneType

        """
        # :raises ValueError: if the message_body exceeds 160 characters
        # :raises TypeError: if the message_body is not a basestring

        self.pin = pin
        self.update_interval = update_interval
        self.save_interval = save_interval
        self.time, self.last_time = (None, None)
        self.value, self.last_value = (None,None)
        self.data = np.empty(0,3)
        self.event_data = np.empty(0,3)
        self.sessionID = str(time.monotonic())
        self.filename = "yeda_" + self.ID + ".csv"
        self.signalID = "eda_" + str(Yeda.n_instances)
        Yeda.n_instances = Yeda.n_instances + 1
        
    def connect(self):
        """
        Connects to the sensor port
        """
        self.sensor = analogio.AnalogIn(self.pin)

    def result(self):
        return (self.time, self.value, self.delta)

    def read(self):
        self.last_time = self.time
        self.time = time.monotonic()

        self.last_value = self.value
        self.value = 65536 / self.sensor.value 
        
        self.delta = self.last_value - self.value
        return self.result()

    def update(self, interval = None, frequency = None):
        """
        Reads the sensor value

        :param interval float: overrides update interval of object
        :param frequency float: overrides interval as reads/s
        :return: tuple (update, value), with the last value if no update has occured.
        """

        ## Catching the method arguments
        if interval is None and frequency is None:
            interval = self.interval
        elif(isinstance(interval, float)):
            interval = interval
        elif(isinstance(frequency, float)):
            interval = 1/frequency

        this_time = time.monotonic()
        if interval > (this_time - self.last_time):
            self.read()
            return (True, self.result())
        else:
            return (False, self.result())

    def record(self):
        np.append(self.data, self.result(), axis=0)

    def record_event(self, label = "TOI", value = 1):
        this_time = time.monotonic()
        np.append(self.event_data, (this_time, str(label), float(value)), 
                  axis=0)

    def reset_data(self):
        self.data = np.empty(0,3)

    def save_data(self):
        if int(time.monotonic()) % self.save_interval == 0: ## Modulo remains
            np.savetxt(self.filename, 
                self.data,
                comments='#',
                delimiter=',',
                header='time,' + self.signalID + ',delta')
            self.reset_data()
    
    def print(self):
        print(self.value)

