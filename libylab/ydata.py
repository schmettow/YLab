import os
import board
import time
import sdcardio
import storage
import busio
from Sensory import this_moment

class Ydata:
    pins = None
    update_interval = 1
    
        
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
 
    def __init__(self, sensor, led = None):
        self.last_saved = None
        self.sensor = sensor
        self.led = led
 
 
    def update(self):
        """
        Saves sensor data on a storage device
        """
        now = this_moment()
        first_save = self.last_saved is None
        if first_save or (now - self.last_saved) >= self.update_interval:
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
    def demo(cls):
        from Sensory import Sensor
        sensor = Sensor()
        sensor.connect()
        cls.init() # for inheritance
        drive = cls(sensor) 
        while True:
            if sensor.sample():
                sensor.record()
            drive.update()
        cls.final()



class SDcard(Ydata):
    pins = {"cs":board.GP15,
            "spi": board.GP10, "mosi": board.GP11, "miso":board.GP12}
    update_interval = 1
    
    @classmethod
    def init(cls):
        cls.spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
        cls.cs = board.GP15
        cls.sd = sdcardio.SDCard(cls.spi, cls.cs)
        cls.vfs = storage.VfsFat(cls.sd)
        return True
    
    
    def connect_(self):
        self.cs = self.pins["cs"]
        try:
            self.spi = busio.SPI(self.pins["spi"], MOSI=self.pins["mosi"], MISO=self.pins["miso"])
            try:
                self.sd = sdcardio.SDCard(self.spi, self.cs)
                try: 
                    self.vfs = storage.VfsFat(sd)
                    storage.mount(vfs, '/sd')
                    return True
                except:
                    print("Mounting failed")
            except:
                print("SD card not discovered")
        except:
            print("SPI failed")
        return False
    
 
    
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
        self.mount_point = "/sd"
        storage.mount(SDcard.vfs, self.mount_point)
        path = self.mount_point + "/ylab.csv"
        if self.last_saved is None:
             mode = "w"
             with open(path, mode) as file:
                 file.write("time,ID,value\n")
        else:
             mode = "a"
             data = self.sensor.data
             n_data = len(data[0])
             with open(path, mode) as file:
                 for row in range(0, n_data):
                     file.write(str(data[0][row]) + "," +
                                str(data[1][row]) +"," +
                                str(data[2][row]) + "\n")
        storage.umount(self.vfs)


    
#     def write(self):
#         # result = np.ones(shape = [2,3]) # Sensor.result()
#         file_name = "ylab.csv"          # Sensor.file_name
#         path = "/sd/" + file_name
#         if self.last_saved is None:
#             mode = "w"
#             with open(path, mode) as file:
#                 file.write("time", "," ,"ID", ",", "value" ,"\n")
#         else:
#             mode = "a"
#             with open(path, mode) as file:
#                 for row in self.sensor.result():
#                     file.write(str(row[0]), "," ,row[1],"," ,str(row[2]),"\n")

        
SDcard.demo()



    
        
    # def reset_data(self):
    #     self.data = np.empty([0,2])

    # def init_storage():
    #     cs = board.GP15
    #     spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
    #     sd = sdcardio.SDCard(spi, cs)
    #     vfs = storage.VfsFat(sd)
    #     storage.mount(vfs, '/sd')
        
    # def release_storage():
    #     storage.umount(vfs)
    #     spi.deinit()
    #     sd.deinit()


    # def save_data(self):
    #     if self.last_saved is None:
    #         mode = "w"
    #     else:
    #         mode = "a"
    #     Yhr.init_storage()
    #     path = os.path.join("/sd", self.filename)
    #     Yhr.release_storage()
        
#         with open(self.filename, mode) as file:
#             for row in self.data:
#                 file.write(row[0], "," ,row[1],"\n")
#        file.close()
    
    # def move_data(self):
    #     now = this_moment()
    #     if self.last_saved is None: # first time
    #         self.save()
    #         self.last_saved = now
    #     if (now - self.last_saved) >= self.save_interval:
    #         # self.save()
    #         self.reset_data()

