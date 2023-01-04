import os
import board
import time
import sdcardio
#import sdioio
import storage
import busio

def this_moment():
    return time.time()

class Ydata:
    pins = None
    save_interval = 1
    filename = None
        
    @classmethod
    def init(cls):
        return True
    
    @classmethod
    def final(cls):
        return True
        
    def connect(self):
        return True
    
    def disconnect(self):
        return True
    
    def write(self, result):
        return True
 
    def __init__(self, sensor, filename = None, save_interval = None, led = None):
        self.last_saved = None
        self.sensor = sensor
        self.led = led
        if not filename is None: self.filename = filename
        if not save_interval is None: self.save_interval = save_interval
 
 
    def update(self):
        """
        Saves sensor data on a storage device
        """
        now = this_moment()
        first_save = self.last_saved is None
        if first_save or (now - self.last_saved) >= self.save_interval:
            self.move()
            self.last_saved = now
            return True
        return False
    
    def move(self):
        self.write()
        self.sensor.reset_data()
        return True
    
    @classmethod
    def demo_0(cls):
        from Sensory import Sensor
        sensor = Sensor()
        sensor.connect()
        
        cls.init() # for inheritance
        drive = cls(sensor, filename = "demo_0.csv")
        drive.connect()
        drive.save_interval = 1
        
        start = this_moment()
        while (this_moment() - start) < 5:
            if sensor.sample():
                print(sensor.buffer())
            if drive.update():
                print("save")
        drive.disconnect()
        cls.final()
    
    
    @classmethod
    def demo_1(cls):
        from sensory import Sensor, Sensory
        sensory = Sensory([Sensor(), Sensor(sample_interval = 0.1)])
        sensory.connect()
        if cls.init(): # for inheritance
            drive = cls(sensory, filename = "demo_1.csv")
            drive.update_interval = 1
            drive.connect()
            start = this_moment()
            while (this_moment - start) > 5:
                if sensory.sample():
                    print(sensory.buffer())
                if drive.update():
                    print("write")
            drive.disconnect()
            cls.final()

class SDcard(Ydata):
    pins = {"cs":board.GP15,
            "spi": board.GP10, "mosi": board.GP11, "miso":board.GP12},
    baudrate = 1E6
    update_interval = 1
    mount_point = "/sd"
    filename = "ylab.csv"
    
    @classmethod
    def init(cls, baudrate = None):
        if not baudrate is None:
            cls.baudrate = baudrate
        cls.spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
        cls.cs = board.GP15
        cls.sd = sdcardio.SDCard(cls.spi, cls.cs,
                                 baudrate = int(cls.baudrate))
        cls.vfs = storage.VfsFat(cls.sd)
        return True
    
    @classmethod
    def final(cls):
        result = True
        try:
            cls.sd.deinit()
        except:
            print("sd deinit failed")
            result = False
        try:
            cls.spi.deinit()
        except:
            print("spi deinit failed")
            result = False
        return result
       
    def connect(self, mount_point = "/sd"):
        self.mount_point = mount_point
        self.filename = None
        try:
            storage.mount(SDcard.vfs, self.mount_point)
        except:
            print("mount failed")
            return(False)
        return(True)

    def create_file(self, filename = None):
        if not filename is None: self.filename = filename
        self.path = self.mount_point + "/" + self.filename
        
        try:
            with open(self.path, "w") as file:
                file.write("time,ID,value\n")
        except:
            return False
        return True
                
    def disconnect(self):
        try: # this makes sure they all run through
            storage.umount(self.vfs) 
        except:
            return False
        return True # <-- quick fix

    def write(self):
        data = self.sensor.data
        n_data = self.sensor.n_obs()
        csv_out = ""
        for row in range(0, n_data):
            csv_out = csv_out + ",".join([	str(data[0][row]),
                                            str(data[1][row]),
                                            str(data[2][row])]) + "\n"
        
        with open(self.path, "a") as file:
            file.write(csv_out)
        return n_data

    def write_(self):
        written_rows = 0
        path = self.path
        mode = "a"
        data = self.sensor.data
        n_data = self.sensor.n_obs()
        with open(path, mode) as file:
            for row in range(0, n_data):
                written_rows += 1
                file.write(str(data[0][row]) + "," +
                           str(data[1][row]) +"," +
                           str(data[2][row]) + "\n")
        return written_rows
       
       
       
class BSU(Ydata):
    """
    Burst Save over USB
    
    sends csv packages up the serial line
    """
    def write(self):
        written_rows = 0
        data = self.sensor.data
        n_data = self.sensor.n_obs()
        for row in range(0, n_data):
            written_rows += 1
            print(  ",".join(  [str(data[0][row]), ## needs to be expanded
                                str(data[1][row]),
                                str(data[2][row])]))
        return written_rows
    
    
