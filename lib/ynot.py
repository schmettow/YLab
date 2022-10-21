import board
import os
import time
import digitalio
from sensory import this_moment, Sensor


class YnotSend:
    
    def __init__(self, pin = board.LED, time_unit = 0.1, pulse_width = 0.01):
        self.pin = pin
        self.pulse_width = pulse_width
        self.time_unit = time_unit
        self.state = "init"
    
    def connect(self, sensor):
        self.out = digitalio.DigitalInOut(self.pin)
        self.out.direction = digitalio.Direction.OUTPUT
        self.out.value = False
        self.sensor = sensor
        self.value = None
        self.state = "connected"

    def update(self):
        now = this_moment()
        if self.state == "connected":
            self.state = "pulse"
            self.on()
            self.time_started = now
            return True
        elif self.state == "pulse" and (now - self.time_started) >= self.pulse_width:
            self.state = "send"
            self.off()
            self.value = self.sensor.read()
            self.duration = self.value * self.time_unit
            self.time_started = now
            return True
        if self.state == "send" and (now - self.time_started) >= self.duration:
            self.state = "pulse"
            self.on()
            self.time_started = now
            return True
        return False
                
    def on(self):
        self.out.value = True
        
    def off(self):
        self.out.value = False
        

def main():
    Sender = YnotSend(pin = board.LED, time_unit = 0.5, pulse_width = 0.1)
    Sensor = Sensor()
    Sender.connect(Sensor)
    while True:
        time.sleep(0.01)
        Sender.update()
        print(int(Sender.out.value))

main()
            
        
        
    
    