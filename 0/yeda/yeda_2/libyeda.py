import board
import os
import time
import analogio
import storage
import busio
import sdcardio
from ulab import numpy as np

def this_moment():
    return time.time()

class Yeda:
    n_instances = int(0)

    def __init__(self,  pin,
                        update_interval, 
                        save_interval):
        """
        Creates a new YEDA sensor object

        :param eda_pin: IO port YEDA is connected to, default is Grove slot 
        :param update_interval float: time between measures
        :param save_interval float: time between pushing the collected data to a file
        :return: None
        :rtype: NoneType

        """

        self.ID = "eda_" + str(Yeda.n_instances) ## auto-counting multiple Yeda devices
        self.pin = pin
        self.update_interval = update_interval
        self.save_interval = save_interval
        self.time, self.last_time = (None, None)
        self.value, self.last_value = (None,None)
        self.data = np.empty([0,2])
        self.sessionID = str(this_moment())
        self.filename = "yeda_" + self.ID + ".npy"     ## CSV file to collect data
        self.last_saved = None
        Yeda.n_instances = Yeda.n_instances + 1        ## auto-counting multiple Yeda devices
        
    def connect(self):
        """
        Connects to the sensor port
        """
        self.sensor = analogio.AnalogIn(self.pin)

    def result(self):
        return (self.time, self.value)

    def read(self):
        now = this_moment()        
        self.last_value = self.value
        self.value = 65536 / self.sensor.value
        if self.time is None: ## the first read
            self.last_time = this_moment
        return self.result()

    def sample(self, interval = None, frequency = None):
        """
        Reads the sensor value

        :param interval float: overrides update interval of object
        :param frequency float: overrides interval as reads/s
        :return: logical value whether an update has been performed
        """

        ## Catching the method arguments
        if interval is None and frequency is None:
            interval = self.update_interval
        elif(isinstance(interval, float)):
            interval = interval
        elif(isinstance(frequency, float)):
            interval = 1/frequency
        else:
            print("sample(): arguments interval and frequency must either be omitted, or used one at a time.")

        now = this_moment()
        if self.time is None: ## first read
            self.read()
        elif interval > (this_moment - self.last_time):
            self.read()
            return True
        else:
            return False

    def record(self):
        np.append(self.data, self.result(), axis=0)

    def record_event(self, label = "MOI", value = 1):
        now = this_moment()
        np.append(self.event_data, (this_moment, str(label), float(value)), 
                  axis=0)

    def reset_data(self):
        self.data = np.empty([0,2])

    def init_storage():
        cs = board.GP15
        spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
        sd = sdcardio.SDCard(spi, cs)
        vfs = storage.VfsFat(sd)
        storage.mount(vfs, '/sd')
        
    def release_storage():
        storage.umount(vfs)
        spi.deinit()
        sd.deinit()


    def save_data(self):
        if self.last_saved is None:
            mode = "w"
        else:
            mode = "a"
        Yeda.init_storage()
        path = os.path.join("/sd", self.filename)
        Yeda.release_storage()
        
#         with open(self.filename, mode) as file:
#             for row in self.data:
#                 file.write(row[0], "," ,row[1],"\n")
#        file.close()
    
    def move_data(self):
        now = time_monotonic()
        if self.last_saved is None: # first time
            self.save()
            self.last_saved = this_moment
        time_since = this_moment - self.last_saved
        if (this_moment() - self.last_saved) >= self.save_interval:
            
                
                self.reset_data()
    
    def print(self):
        # out = self.ID +":"+ self.value
        out = self.value
        print(out)
        



