"""
YUI is your User Interface
"""


import board
import time
def this_moment():
    return time.monotonic()
import digitalio
from neopixel_write import neopixel_write

print("YUI")

   

class Output:
    pins = {}
    def __init__(self, pins = None):
        if not pins is None:
            self.pins = pins
    
    def connect(self):
        return True
    
    def write():
        pass

class LED(Output):
    pins = board.LED
       
    def connect(self):
        self.led = digitalio.DigitalInOut(self.pins)
        self.led.direction = digitalio.Direction.OUTPUT
        
    def write(self, value):
        self.led.value = value
        
    def on(self):
        self.write(True)
        
    def off(self):
        self.write(False)
        
    def toggle(self):
        self.led.value = not self.led.value

class RGB(Output):
    pins = board.GP28
    white = bytearray([10, 10, 10])
    red   = bytearray([0, 10, 0])
    green = bytearray([5, 0, 0])
    blue  = bytearray([0, 0, 3])
    black  = bytearray([0, 0, 0])
    
    def __init__(self, pins = None):
        if not pins is None:
            self.pins = pins
            
    def connect(self):
        self.led = digitalio.DigitalInOut(self.pins)
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


class Input:
    pins = {"yellow": 0,
            "white":  1}
    sample_interval = 0.05
    
    def __init__(self, pins = None, sample_interval = None):
        if pins is not None:
            self.pins = pins
        if sample_interval is not None:
            self.sample_interval = sample_interval
    
    def connect(self):
        try:
            self.time = this_moment()
            self.value = self.read()
            return True
        except:
            print("First read failed.")
            return False
            
    def read(self):
        return 1 + int(this_moment()) % 42

    def update(self): # update only happens when a state change occurs
        now = this_moment()
        time_passed = now - self.time
        if time_passed > self.sample_interval:
            new_value = self.read()
            if new_value != self.value: # <---
                self.last_value = self.value
                self.value = new_value
                self.last_time = self.time
                self.time = now
                return True
        return False
        
    def demo():
        In = Input()
        In.connect()
        while True:
            if In.update():
                print(In.value)

class Onoff(Input):
    pins = board.GP20
    
    def connect(self):
        self.sensor = digitalio.DigitalInOut(self.pins)
        self.sensor.switch_to_input(pull=digitalio.Pull.DOWN)
        return Input.connect(self)
    
    def read(self):
        return not self.sensor.value
    
    def demo():
        Ono = Onoff()
        if Ono.connect():
            while True:
                if Ono.update():
                    print(Ono.value)
            


class Toggle(Onoff):
    
    def connect(self):
        if Onoff.connect(self):    
            self.state = False # <---
            return True
        else:
            return False
  
    def update_state(self):
        if self.value: # on press
            self.state = not self.state # toggle
            return True
        return False
    
    def demo():
        Tgl = Toggle()
        if Tgl.connect():
            while True:
                if Tgl.update():
                    if Tgl.update_state():
                        print(Tgl.state)


        

class Button(Onoff):
    long_press = 1.0

    def connect(self):
        if Onoff.connect(self):    
            self.event  = None
            return True
        else:
            return False

    
    
    def update_event(self):
        if not self.value: # on release
            if (self.time - self.last_time) < self.long_press:
                self.event = "short"
                return True
            else:
                self.event = "long"
                return True
        return False


    def demo():
        Btn = Button()
        Btn.connect()
        Btn.long_press = 1.2
        STATE = "Stop"
        print(STATE)
        ## Fast while loop
        while True:
            if Btn.update():
                if Btn.update_event():
                    if Btn.event == "short":
                        if STATE == "Stop" or STATE == "Pause":
                            STATE = "Record"
                        elif STATE == "Record":
                            STATE = "Pause"
                    elif Btn.event == "long":
                        STATE = "Stop"
                    print(Btn.event + " --> " + STATE)

