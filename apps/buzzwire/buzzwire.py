"""
YLab: Buzzwire task with one buzz contact and one base station contact,
plus Yema, Yxz and environmental sensors

Setup:

YEMA:  Grove 6 (analog)
YEMA_ads:  Grove 4 (I2C)
DHT11: Grove 2
Buzzwire: Grove 1

"""

import board
import time

from sensory import Sensory, ContactEvent, MOI, Yxz_6D, Yema, Yema_ads, ADS, DHT11
from yui import Shortlong, RGB, Buzz, LED
from ydata import SDcard, BSU, Ydt

def make_filename():
    return "ylab_buzzwire" + str(time.time()) + ".ydt"

def main():
    wire = ContactEvent(ID = "buzz",
                   pins = board.GP0,
                   sample_interval = 1/50)   ## Grove 1
    station = ContactEvent(ID = "station",
                           pins = board.GP1,
                           sample_interval = 1/5) ## Grove 1
    #sensory = DHT11()
    #ads = ADS()
    
    sensory = Sensory( [wire,
                        station,
                        MOI(pins = board.GP21),
                        MOI(pins = board.GP22, ID = "stop"),
                        #DHT11(),
                        Yema(sample_interval = 1/50),
#                         Yema_ads(ads = ADS(),
#                                  sample_interval = 1/50)
                        ])
    
    # sensory = Yema(sample_interval = 1/100)
    
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
                        drive = Ydt(sensory, save_interval = 1)
                        #drive.save_interval = 0.5
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
                sensory.buffer()
                buzzer.switch(wire.value)
            n_obs = drive.update()
            if n_obs:
                print(n_obs)
        elif State == "Pause":
            if sensory.sample():
                sensory.print()
                buzzer.switch(wire.value)
        elif State == "Send":
            if sensory.sample():
                sensory.buffer()
                buzzer.switch(wire.value)
            usb_up.update()
        else:
            pass

main()



