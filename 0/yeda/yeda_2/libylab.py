"""
Provides interaction objects for YLab development
"""


import board
import time
def this_moment():
    return time.monotonic()
import digitalio
from neopixel_write import neopixel_write

print("YLab0")


class Led:
    pin = board.LED
    
    def __init__(self, pin = None):
        if not pin is None:
            self.pin = pin
    
    def connect(self):
        self.led = digitalio.DigitalInOut(self.pin)
        self.led.direction = digitalio.Direction.OUTPUT

    def on(self):
        self.led.value = True
        
    def off(self):
        self.led.value = False
        
    def toggle(self):
        self.led.value = not self.led.value



    

class Button:
    interval = 0.05
    pin = board.GP20
    long_press = 1.0
    debug = True
    
    
    
    def __init__(self, pin = None, interval = None, long_press = None):
        if pin is not None:
            self.pin = pin
        if interval is not None:
            self.interval = interval
        if long_press is not None:
            self.long_press = long_press
    
    
    def debug(self, msg, condition = True):
        if self.debug and condition:
            print(msg)
    
    def connect(self):
        self.sensor = digitalio.DigitalInOut(self.pin)
        self.sensor.switch_to_input(pull=digitalio.Pull.DOWN)
        self.value = self.last_value = self.read()
        self.time = self.event_time = this_moment()
        self.event = self.last_event = None
        self.debug("connected")
    
    def read(self):
        return not self.sensor.value
    
    def sample(self):
        now = this_moment()
        time_passed = now - self.time
        if time_passed > self.interval:
            self.time = now
            new_value = self.read()
            if new_value != self.value:
                self.last_value = self.value
                self.value = new_value
                return True
        return False
    
    def update_event(self):
        now = this_moment()
        if not self.value == self.last_value:
            self.last_event_time = self.event_time
            self.event_time = now
            if not self.value: # on release
                if (self.event_time - self.last_event_time) < self.long_press:
                    self.event = "short"
                    return True
                else:
                    self.event = "long"
                    return True
        return False


    def demo(pin = board.GP20):
        BTN = Button(pin, 0.1, 1)
        BTN.connect()
        Rgb = RGB()
        Rgb.connect()
        # neopixel_write(Rgb.led, bytearray([2,2,2]))
        Rgb.white()
        STATE = "Stop"
        print(STATE)
        cnt = 0
        ## Fast while loop
        while True:
            if BTN.sample():
                if BTN.update_event():
                    if BTN.event == "short":
                        if STATE == "Stop" or STATE == "Pause":
                            STATE = "Record"
                        elif STATE == "Record":
                            STATE = "Pause"
                    elif BTN.event == "long":
                        STATE = "Stop"
                    print(BTN.event + " --> " + STATE)
                    
                    if STATE == "Stop":
                        Rgb.white()
                    elif STATE == "Record":
                        Rgb.red()
                    elif STATE == "Pause":
                        Rgb.green()


class RGB:
    pin = board.GP28
    white = bytearray([10, 10, 10])
    red   = bytearray([0, 10, 0])
    green = bytearray([5, 0, 0])
    blue  = bytearray([0, 0, 3])
    black  = bytearray([0, 0, 0])
    
    def __init__(self, pin = None):
        if not pin is None:
            self.pin = pin
            
    def connect(self):
        self.led = digitalio.DigitalInOut(self.pin)
        self.led.direction = digitalio.Direction.OUTPUT

    def write(self, color):
        neopixel_write(self.led, color)
        
    def red(self):
        self.write(bytearray([0, 10, 0]))
    
    def green(self):
        self.write(bytearray([5, 0, 0]))
    
    def blue(self):
        self.write(bytearray([0, 0, 3]))
    
    def white(self):
        self.write(bytearray([10, 10, 10]))
        
    def off(self):
        self.write(bytearray([0, 0, 0]))


Button.demo() 
