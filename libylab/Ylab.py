import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from ulab import numpy as np

def this_moment():
    return time.monotonic()

class Sensor:
    n_instances = int(0)
    sample_interval = 0.1
    save_interval = 2

    def __init__(self,  pins = None,
                        sample_interval = None, 
                        save_interval = None):
        """
        Creates a new Yhr sensor object

        :param eda_pin: IO port Yhr is connected to, default is Grove slot 
        :param sample_interval float: time between measures
        :param save_interval float: time between pushing the collected data to a file
        :return: None
        :rtype: NoneType

        """
        if not pins is None:
            self.pins = pins
        if not sample_interval is None:
            self.sample_interval = sample_interval
        if not save_interval is None:
            self.save_interval = save_interval
        self.sensor_class = self.__class__.__name__
        self.ID = self.sensor_class + str(Yhr.n_instances) ## auto-counting multiple devices
        self.time = this_moment()
        self.value = float()
        self.data = np.zeros((0,2))
        self.sessionID = str(this_moment())
        self.filename = "Yhr_" + self.ID + ".npy"     ## CSV file to collect data
        self.last_saved = None
        Sensor.n_instances = Sensor.n_instances + 1        ## auto-counting multiple Yhr devices
    

    def sample(self, interval = None):
        """
        Updates the sensor readings in regular intervals
        
        For this it needs to be in a fast while loop
        
        :param interval float: overrides update interval of object
        :param frequency float: overrides interval as reads/s
        :return: tuple (update, value), with the last value if no update has occured.
        """

        ## Catching the method arguments
        if interval is not None:
            self.sample_interval = interval
        
        now = this_moment()
        if (now - self.time) > self.sample_interval:
            self.time = now
            self.value = self.read()
            return True
        else:
            return False

    def result(self):
        """
        Presents the current reading
        
        ... in YLab standard, which is time, ID, value

        :return: (time, ID, value)
        :rtype: tuple

        """
        return np.array((self.time, self.value)).reshape((1, 2))


    def record(self):
        np.concatenate((self.data,  self.result()), axis=0)

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
        Yhr.init_storage()
        path = os.path.join("/sd", self.filename)
        Yhr.release_storage()
        
#         with open(self.filename, mode) as file:
#             for row in self.data:
#                 file.write(row[0], "," ,row[1],"\n")
#        file.close()
    
    def move_data(self):
        now = this_moment()
        if self.last_saved is None: # first time
            self.save()
            self.last_saved = now
        if (now - self.last_saved) >= self.save_interval:
            # self.save()
            self.reset_data()
    
    def print(self):
        out = self.ID +":"+ str(self.value)
        print(out)
        

    
class Yeda(Sensor):
    def connect(self):
        """
        Connects to the sensor port
        """
        self.sensor = analogio.AnalogIn(self.pin)

    def read(self):
        now = this_moment()        
        self.last_value = self.value
        self.value = 65536 / self.sensor.value
        if self.time is None: ## the first read
            self.last_time = this_moment
        return self.result()



class Yhr(Sensor):
    pins = {"SCL": board.GP7,
            "SDA": board.GP6}
        
    def connect(self):
        """
        Connects to the sensor port
        :return: success  or fail
        :rtype: Boolean
        """
        i2c = busio.I2C(self.pins["SCL"],
                        self.pins["SDA"])
        ads = ADS.ADS1115(i2c)
        self.sensor = AnalogIn(ads, ADS.P0)
        value = None
        try:
            value = self.sensor.value
        except:
            print("Failed first read.")
        if value is None:
            return False
        else:
            self.value = value
            self.time = this_moment()
            return True

    def read(self):
        """
        Connects to the sensor port
        :return: sensor reading
        :rtype: float
        """
        return self.sensor.value

    def demo(self):
        while True:
            if self.sample():
                self.print()
            