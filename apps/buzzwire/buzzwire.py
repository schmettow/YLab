"""
YLab: Buzzwire task with one buzz contact and one base station contact,
plus Yema, Yxz and environmental sensors

Setup:

YEMA:  Grove 6 (analog)
Yxz:   Grove 4 (I2C)
DHT11: Grove 2
Buzzwire: Grove 1

"""

import board
import time

from sensory import Sensory, ContactEvent, MOI, Yxz_3D, Yema, DHT11
from yui import Shortlong, RGB, Buzz, LED
from ydata import SDcard, BSU

def make_filename():
    return "ylab_buzzwire" + str(time.time()) + ".csv"

def main():
    wire = ContactEvent(ID = "buzz",
                   pins = board.GP0,
                   sample_interval = 1/50)   ## Grove 1
    station = ContactEvent(ID = "station",
                           pins = board.GP1,
                           sample_interval = 1/5) ## Grove 1
    #sensory = DHT11()
    sensory = Sensory( [wire,
                        station,
                        MOI(pins = board.GP21),
                        MOI(pins = board.GP22, ID = "stop"),
                        DHT11(),
                        Yema(sample_interval = 1/50),
                        Yxz_3D(sample_interval = 1/10)])
    sensory.connect()
        
    led = LED()
    btn = Shortlong()
    rgb = RGB()
    buzzer = Buzz() ## used as continuous feedback
    
    for ui_element in [led, rgb, btn, buzzer]:
        ui_element.connect()
    
    State = "Stop"
    rgb.white()
    buzzer.off()
        
    ## Fast while loop
    while True:
        ################ Interactive transitionals #############
        if btn.update():
            if btn.update_event():
                # short press
                if btn.event == "short":
                    ## Stop --> Pause
                    if State == "Stop":
                        rgb.green()
                        sensory.clear_buffer()
                        SDcard.init(baudrate = 3E7)
                        drive = SDcard(sensory)
                        drive.save_interval = 5
                        drive.connect()
                        drive.create_file(make_filename())
                        State = "Pause"
                    ## Record --> Pause
                    elif State == "Record":
                        rgb.green()
                        State = "Pause"
                    ## Pause --> Record
                    elif State == "Pause":
                        rgb.red()
                        State = "Record"
                # long press
                elif btn.event == "long":
                    ## --> STOP
                    if State == "Pause" or State == "Record":
                        drive.disconnect()
                        SDcard.final()
                        rgb.white()
                        buzzer.off()
                        State = "Stop"
                    ## <--> Toggle STOP and SEND
                    elif State == "Stop":
                        usb_up = BSU(sensory)
                        usb_up.save_interval = 0 ## continuous
                        rgb.blue()
                        State = "Send"
                    elif State == "Send":
                        rgb.white()
                        State = "Stop"

        ################ Continuous processing #############

        if State == "Record":
            if sensory.sample():
                sensory.print()
                sensory.buffer()
                buzzer.switch(wire.value)
            drive.update()
        elif State == "Pause":
            if sensory.sample():
                sensory.print()
                buzzer.switch(wire.value)
        elif State == "Send":
            if sensory.sample():
                sensory.buffer()
                buzzer.switch(wire.value)
            if usb_up.update():
                sensory.clear_buffer()
        else:
            pass

main()



