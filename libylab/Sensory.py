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
    sample_interval = 1.0/4
    pins = None

    def __init__(self,  pins = None,
                        sample_interval = None):
        """
        Creates a new YedaADS sensor object

        :param eda_pin: IO port YedaADS is connected to, default is Grove slot 
        :param sample_interval float: time between measures
        :return: None
        :rtype: NoneType

        """
        if not pins is None:
            self.pins = pins
        if not sample_interval is None:
            self.sample_interval = sample_interval
        self.sensor_class = self.__class__.__name__
        self.ID = self.sensor_class + str(Sensor.n_instances) ## auto-counting multiple devices
        self.time = this_moment()
        self.value = float()
        self.data = [[],[],[]]
        self.last_saved = None
        Sensor.n_instances = Sensor.n_instances + 1        ## auto-counting multiple Sensor devices
    
    def connect(self):
        try:
            self.value = self.read()
            self.time = this_moment()
            return True
        except:
            print("Failed first read.")
            return False
    
    def read(self):
        return self.time % 42

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
        if (now - self.time) >= self.sample_interval:
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
        if isinstance(self.time, (list, tuple)):
            out = [self.time, self.ID, self.value]
        else:
            out = [[self.time], [self.ID], [self.value]]
        return out

    def buffer(self):
        result = self.result()
        n_result = len(result[0])
        for col in range(0, len(result)):
            self.data[col].append(result[col][0])  ## <<- bad fix
        return n_result
    
    def record(self):
        return self.buffer()
   
    def data_dim(self):
        return (len(self.data[0]), len(self.data))
   
    def n_obs(self):
        return len(self.data[0])
    
    def print(self):
        out = self.ID +":"+ str(self.value)
        print(out)

    @classmethod
    def demo(cls):
        sensor = cls()
        sensor.connect()
        sensor.sample_interval = 0.2
        while True:
            if sensor.sample():
                sensor.print()
                print(sensor.result())
    def reset_data(self):
        self.data = [[], [], []]
        return True




class Sensory(Sensor):
    """
    A sensor array
    
    """
    
    
    
    def __init__(self, sensor_array):
        self.sensors = sensor_array
        self.ID = []
        self.time = []
        self.value = []
        self.data = [[],[],[]]
    
    def connect(self):
        success = True
        for sensor in self.sensors:
            if not sensor.connect():
                success = false
        return success
        
    def sample(self):
        self.ID = []
        self.time = []
        self.value = []
        new_sample = 0
        for sensor in self.sensors:
            if sensor.sample():
                self.ID.append(sensor.ID)
                self.time.append(sensor.time)
                self.value.append(sensor.value)
                new_sample += 1
        return new_sample
    
         
    def print(self):
        out_string = ""
        for sensor in self.sensors:
            out_string = out_string + sensor.ID + ":" + str(sensor.value) + " "
        print(out_string)
        return True
    
    


class AnalogSensor(Sensor):
    pins = board.GP27
    bit_width = 11
    reciprocal = False
    
    def connect(self):
        import analogio
        """
        Connects to the sensor port
        """
        self.sensor = analogio.AnalogIn(self.pins)
        return Sensor.connect(self)

    def read(self):
        raw_value = self.sensor.value
        if not raw_value == 0:
            value = 2**self.bit_width / raw_value
        else:
            value = 2**self.bit_width
        if not self.reciprocal:
            return value
        else:
            return 1/value



class SensorADS(AnalogSensor):
    pins = {"SCL": board.GP7,
            "SDA": board.GP6}
    bit_width = 15
    reciprocal = False
    i2c = None
    ads = None
    
    def init_i2c():
        SensorADS.i2c = busio.I2C(SensorADS.pins["SCL"],
                                  SensorADS.pins["SDA"])
        
    def init_ads():
        SensorADS.ads = ADS.ADS1115(SensorADS.i2c)
    
    def connect(self):
        """
        Connects to the sensor port
        :return: success  or fail
        :rtype: Boolean
        """
        
        if SensorADS.i2c is None:
            SensorADS.init_i2c()
            print("Init I2C")
        if SensorADS.ads is None:
            SensorADS.init_ads()
            print("Init ADS")
        
        self.sensor = AnalogIn(SensorADS.ads, ADS.P0)
        return Sensor.connect(self)


class Yeda(AnalogSensor):
    pins = board.GP27
    reciprocal = True

class Yema(SensorADS):
    reciprocal = True


