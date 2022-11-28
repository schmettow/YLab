import board
import time
import busio

def this_moment():
    return time.monotonic()

class Sensor:
    """
    provides a unified interface for sampling from sensors
    """
    n_instances = int(0)
    sample_interval = 1.0/4
    pins = None
    
    def __init__(self,
                 ID = None,
                 pins = None,
                 sample_interval = None,
                 channel = 0):
        """
        Creates a new sensor object

        :param pins: IO port
        :param sample_interval float: time between measures
        :return: None
        :rtype: NoneType

        """
        self.channel = channel
        if not pins is None:
            self.pins = pins
        if not sample_interval is None:
            self.sample_interval = sample_interval
        self.sensor_class = self.__class__.__name__
        self.ID = self.sensor_class + str(self.__class__.n_instances)
        
        
        self.time = this_moment()
        self.value = float()
        self.reset_data()
        self.last_saved = None
        self.__class__.n_instances += 1      ## auto-counting multiple Sensors
    
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
        Presents the current reading as YLab standard measure (time, ID, value)

        :return: (time, ID, value)
        :rtype: tuple

        """
        if isinstance(self.time, (list, tuple)):
            out = [self.time, self.ID, self.value]
        else:
            out = [[self.time], [self.ID], [self.value]]
        return out

    def clear_buffer(self):
        """
        resets the sensor buffer
        """
        self.data = [[], [], []]
        return True

    def buffer(self):
        """
        adds a measurement to the sensor buffer
        """
        result = self.result()
        n_result = len(result[0])
        for col in range(0, len(result)):
            self.data[col].append(result[col][0])  ## <<- bad fix
        return n_result
    
    ## just for backward compatibility
    def reset_data(self):        
        return self.clear_buffer()
    
    def record(self):
        return self.buffer()
    
    def data_dim(self):
        return (len(self.data[0]), len(self.data))
   
    def n_obs(self):
        return len(self.data[0])
    
    def print(self):
        """
        Print the present measure for use with Thonny plotter
        """
        out = self.ID +":"+ str(self.value)
        print(out)

    @classmethod
    def demo_0(cls):
        """
        Basic demo showing sampling and printing
        """
        sensor = cls()
        sensor.connect()
        sensor.sample_interval = 0.1
        while True:
            if sensor.sample():
                sensor.print()
                
    @classmethod
    def demo_1(cls):
        from ydata import SDcard
        """
        Demo of storage (SD card required)
        """
        sensor = cls()
        sensor.connect()
        sensor.sample_interval = 0.1
        
        SDcard.init()
        drive = SDcard(sensor, "sensor_demo_1.csv")
        drive.connect()
        
        while True:
            if sensor.sample():
                sensor.print()
                sensor.buffer()
                print(sensor.result())
            drive.update()



class Sensory(Sensor):
    """
    Unifying multiple sensors in a sensor array

    :param list of sensor objects
    """

    def __init__(self, sensor_array):
        self.sensors = sensor_array
        self.ID = []
        self.time = []
        self.value = []
        self.data = [[],[],[]]
    
    def connect(self):
        """
        connect all sensors in the array
        """
        success = True
        for sensor in self.sensors:
            if not sensor.connect():
                success = False
        return success
        
    def sample(self):
        """
        sample all sensors in the array
        """
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
        """
        print readings from all sensors in the array
        """
        out_string = ""
        for sensor in self.sensors:
            out_string = out_string + sensor.ID + ":" + str(sensor.value) + " "
        print(out_string)
        return True
    
    


class Sensor_analog(Sensor):
    pins = board.GP27  ## default is Grove 6
    bit_width = 11
    reciprocal = False
    
    def connect(self):
        import analogio
        self.sensor = analogio.AnalogIn(self.pins)
        return Sensor.connect(self)

    def read(self):
        raw_value = self.sensor.value
        if not raw_value == 0:
            value = 2**self.bit_width / raw_value
        else:
            value = 2**self.bit_width
        if self.reciprocal: value = 1/value
        return 1/value


class ADS():
    pins = {"SCL": board.GP7,
            "SDA": board.GP6}
    bit_width = 15
    i2c = None
    ads = None
    init = False
    data_rate = 860
    mode = 0
    # channels = [ADS.P0, ADS.P1, ADS.P2, ADS.P3]
    
    def __init__(self, gain = 1):
        self.gain = gain
        self.init_i2c()
        print("Init I2C")
        self.init_ads()
        print("Init ADS")
        self.init = True
    
    def init_i2c(self):
        self.i2c = busio.I2C(self.pins["SCL"], 
                             self.pins["SDA"])
        return True
    
    def init_ads(self):
        import adafruit_ads1x15.ads1115 as ads
        self.ads = ads.ADS1115(self.i2c,
                               data_rate = self.data_rate, # max
                               mode = self.mode,
                               gain = self.gain) # cont
        return True
    

class Sensor_ads(Sensor_analog):
    def __init__(self,
                 ads,
                 channel = 0,
                 ID = None,
                 pins = None,
                 sample_interval = None):
        self.ads = ads
        self.channel = channel
        Sensor.__init__(self,
                        ID = ID,
                        pins = pins,
                        sample_interval = sample_interval)
        
    
    def connect(self):
        """
        Connects to an ADS1115 analog pin
        
        :return: success  or fail
        :rtype: Boolean
        """
        
        if self.ads.init:
            from adafruit_ads1x15.analog_in import AnalogIn
            ads = self.ads.ads
            #chan = self.ads.P0 #[ADS.P0, ADS.P1, ADS.P2, ADS.P3][self.channel]
            self.sensor = AnalogIn(ads, self.channel)
            return Sensor.connect(self) ## base class, performs first read
        return False


class Yxz_3D(Sensor):
    pins = {"SCL": board.GP7,
            "SDA": board.GP6}
    i2c_addr = 0x19
    
    def connect(self):
        """
        Connects to an LIS3DH 3 DoF sensor
        
        :return: success  or fail
        :rtype: Boolean
        """
        import adafruit_lis3dh as HAL ## hardware abstraction layer

        self.i2c = busio.I2C(board.GP7, board.GP6)
        self.sensor = self.HAL.LIS3DH_I2C(self.i2c,
                                        address = self.i2c_addr)
        self.sensor.range = self.HAL.RANGE_2_G
        return Sensor.connect(self) ## base class, performs first read

    def read(self):
        accel = [value / self.HAL.STANDARD_GRAVITY for value in self.sensor.acceleration]
        return accel
    
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
        return [[self.time, self.time, self.time],
                [self.ID + axis for axis in ("x","y","z")],
                self.value]




class Sensor_binary(Sensor):
    pins = board.GP22  ## default button GP22 (corner)
    bit_width = 1
    inverted = True
    
    def connect(self):
        import digitalio
        """
        Connects to the sensor port
        """
        self.sensor = digitalio.DigitalIn(self.pins)
        self.sensor.switch_to_input(pull=digitalio.Pull.DOWN)
        return Sensor.connect(self)

    def read(self):
        value = self.sensor.value
        if self.inverted: value = not bool(value)
        return value



class MOI(Sensor):
    """
    Basic moments-of-interest sampler
    
    The MOI sampler has a modified sample() method,
    which only fires, if a defined event has been detected.
    Defaults to button GP22
    """
    sample_interval = 0.01
    pins = board.GP22
    on_on = True
    event = 0
    last_state = state = None
    
    
    def sample(self, interval = None):
        """
        Updates only if the state has changed
        """
        if interval is not None:
            self.sample_interval = interval
        
        now = this_moment()
        if (now - self.time) >= self.sample_interval:
            self.last_state = self.state
            self.state = self.read()
            self.time = now
            if self.state != self.last_state:
                return self.get_event()
        return False

    def connect(self):
        import yui
        if yui.Onoff.connect(self):
            self.value = 0
            return True
        return False
        
    
    def read(self):
        return not self.sensor.value

    def get_event(self):
        if self.state and self.on_on:
            self.value = 1
            return True
        elif not self.state and not self.on_on:
            self.value = 0
            return True
        return False



# MOI.demo_1()



class Yeda(Sensor_analog):
    pins = board.GP27
    reciprocal = True

class Yema(Sensor_analog):
    pins = board.GP27
    sample_interval = 1.0/100
    reciprocal = False
    
class Yema_ads(Sensor_ads):
    sample_interval = 1.0/100
    reciprocal = False

print("Sensory")
