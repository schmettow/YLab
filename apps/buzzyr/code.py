"""
YLab: Buzzwire task with one buzz contact and one base station contact,
plus Yema, Yxz and environmental sensors

Setup:

YEMA, Yeda:  		  Grove 6 (analog)
Buzzwire, Station:    Grove 1

"""

import board
import time

from sensory import Sensory, ContactEvent, MOI, Yema, Yeda, Yxz_6D
from yui import Shortlong, RGB, Buzz, LED
from ydata import BSU

def main():
    wire = ContactEvent(ID = "buzz",
                   pins = board.GP0,
                   sample_interval = 1/100)   ## Grove 1
    station = ContactEvent(ID = "station",
                           pins = board.GP1,
                           sample_interval = 1/5) ## Grove 1    
    sensory = Sensory( [wire,
                        station,
                        MOI(pins = board.GP21),
                        MOI(pins = board.GP22, ID = "stop"),
                        Yeda(sample_interval = 1/5),
                        Yema(sample_interval = 1/10),
                        Yxz_6D(sample_interval = 1/10)
                        ])
    
    sensory.connect()
    usb = BSU(sensory)
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
                    ## Stop --> Active
                    if State == "Stop":
                        rgb.green()
                        sensory.clear_buffer()
                        State = "Active"
                    ## Record --> Active
                    elif State == "Record":
                        rgb.green()
                        State = "Active"
                    ## Active --> Record
                    elif State == "Active":
                        rgb.red()
                        State = "Record"
                # long press
                elif btn.event == "long":
                    ## --> STOP
                    if State == "Active" or State == "Record":
                        rgb.white()
                        buzzer.off()
                        State = "Stop"
                    elif State == "Stop":
                        State = "Record"
                    
        ################ Continuous processing #############q

        if State == "Record":
            if sensory.sample():
                sensory.buffer()
                buzzer.switch(wire.value)
                usb.update()
                
        elif State == "Active":
            if sensory.sample():
                sensory.print()
                buzzer.switch(wire.value)
        else:
            pass

main()