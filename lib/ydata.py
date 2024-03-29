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
        return 0
 
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
            n_obs = self.move()
            self.last_saved = now
            return n_obs
        return 0
    
    def move(self):
        n_obs = self.write()
        self.sensor.clear_buffer()
        return n_obs
    
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
        return True

    def write(self):
        buffer = self.sensor.data
        n_buffer = self.sensor.n_obs()
        csv_out = ""
        for row in range(0, n_buffer):
            csv_out = csv_out + ",".join([	str(buffer[0][row]),
                                            str(buffer[1][row]),
                                            str(buffer[2][row])]) + "\n"
        
        with open(self.path, "a") as file:
            file.write(csv_out)
        return n_buffer

       
class Ydt(SDcard):
    """
    Saves data in binary to sd card.
    
    This is about four times faster than writing CSV.
    The disadvantage is that data needs to be unpacked
    before it can be worked with.
    """
    from struct import pack, unpack
    ydt_format = "@fif"

    def pack_row(row):
        return Ydt.pack(Ydt.ydt_format, row[0], row[1], row[2])

    def unpack_row(row):
        return Ydt.unpack(Ydt.ydt_format, row)
    
    def pack_ydt(buffer):
        out = bytearray()
        for row in range(0, len(buffer[0])):
            this_row = (buffer[0][row],
                        buffer[1][row],
                        buffer[2][row]) 
            out.extend(Ydt.pack_row(this_row))
        return out

    def create_file(self, filename = None):
        if not filename is None: self.filename = filename
        self.path = self.mount_point + "/" + self.filename
        
        try:
            with open(self.path, "wb") as file:
                pass
        except:
            return False
        return True

    def write(self):
        pdata = Ydt.pack_ydt(self.sensor.data)
        with open(self.path, "ab") as file:
            file.write(pdata)
        return self.sensor.n_obs()

    def load_ydt(path):
        out = []
        with open(path, "rb") as file:
            pdata = file.read()
        pdata = Ydt.unpack(Ydt.ydt_format, pdata)
        for row in pdata:
            out.append(row)
        return out



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
    
    
