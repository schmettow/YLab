import os
import board
import time
import sdcardio
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
        if result is None:
            print(result)
        else:
            self.sensor.print()
        time.sleep(0.05)
        return 42
 
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
            if self.connect():
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
        if cls.init(): # for inheritance
            drive = cls(sensor, filename = "demo_0.csv") 
            while True:
                if sensor.sample():
                    print(sensor.buffer())
                drive.update()
            cls.final()
    
    
    @classmethod
    def demo_1(cls):
        from Sensory import Sensor, Sensory
        sensory = Sensory([Sensor(), Sensor(sample_interval = 0.1)])
        sensory.connect()
        if cls.init(): # for inheritance
            drive = cls(sensory, filename = "demo_1.csv")
            while True:
                if sensory.sample():
                    print(sensory.buffer())
                if drive.update():
                    print("write")
            cls.final()

class SDcard(Ydata):
    pins = {"cs":board.GP15,
            "spi": board.GP10, "mosi": board.GP11, "miso":board.GP12}
    update_interval = 1
    filename = "Ylab.csv"
    
    @classmethod
    def init(cls):
        cls.spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
        cls.cs = board.GP15
        cls.sd = sdcardio.SDCard(cls.spi, cls.cs)
        cls.vfs = storage.VfsFat(cls.sd)
        return True
       
    def disconnect_(self):
        try: # this makes sure they all run through
            storage.umount(self.vfs) 
        except:
            print("umount failed")
        try:
            self.spi.deinit()
        except:
            print("sd deinit failed")
        try:
            self.sd.deinit()
        except:
            print("sd deinit failed")
        return True # <-- quick fix

    def write(self):
        written_rows = 0
        self.mount_point = "/sd"
        storage.mount(SDcard.vfs, self.mount_point)
        path = self.mount_point + "/" + self.filename
        if self.last_saved is None:
             mode = "w"
             with open(path, mode) as file:
                 file.write("time,ID,value\n")
        else:
             mode = "a"
             data = self.sensor.data
             n_data = self.sensor.n_obs()
             with open(path, mode) as file:
                 for row in range(0, n_data):
                     written_rows += 1
                     file.write(str(data[0][row]) + "," +
                                str(data[1][row]) +"," +
                                str(data[2][row]) + "\n")
        storage.umount(self.vfs)
        return written_rows

    
