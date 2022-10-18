"""
Yhr is your heart rate
"""

import board
import os
import time
import analogio
import storage
import busio
import sdcardio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from ulab import numpy as np

from libylab import Button, RGB
from libyhr import Yhr

def this_moment():
    return time.monotonic()

HZ = 10 ## sampling frequency in Hz
UPDATE = 1/HZ
PINS = {"SCL": board.GP7,
        "SDA": board.GP6}
SAVE = 1
PRINT = False


print("Yhr is your heart rate monitor")

Yhr_0 = Yhr(pins = PINS,
            sample_interval = UPDATE,
            save_interval = SAVE)
try:
    Yhr_0.connect()
except:
    print("Error: Could not connect Yhr_0.")

BT2 = Button(pin = board.GP20)
BT2.connect()

Rgb = RGB()
Rgb.connect()
Rgb.white()

STATE = "Stop"
print(STATE)


## Fast while loop
while True:
    now = this_moment()  ## this time
            
    ################ Interactive transitionals #############


    # Note that RGB is static. You write a value and it stays. 
    # No need to create presentitionals. The order of the 
    # inner  conditions is completely arbitrary. The order is entirely
    # determined by transitions.
    
    if BT2.sample(): # ha sthe state changed?
        if BT2.update_event(): # has there be a new event?
            if BT2.event == "short":
                ## Record --> Pause
                if STATE == "Record":
                    STATE = "Pause"
                ## Pause --> Record
                elif STATE == "Pause":
                    STATE = "Record"
                ## Stop --> Record
                elif STATE == "Stop":
                    Yhr_0.reset_data()
                    STATE = "Record"
                ## --> STOP
            elif BT2.event == "long":
                STATE = "Stop"
                #Yhr_0.save_data()
            
            ## Updating the static displays ##
            if STATE == "Record":
                Rgb.red()
            elif STATE == "Pause":
                Rgb.green()
            elif STATE == "Stop":
                Rgb.white()
            
        print(STATE)
        

    ################ Continuous processing #############

    if STATE == "Record":
        if Yhr_0.sample():
            Yhr_0.record()
            #Yhr_0.save_data()
    elif STATE == "Pause":
        Yhr_0.sample()
        #Yhr_0.print()
    elif STATE == "Stop":
        pass
    else:
        pass

    ################ Presentitionals #############
    # Since we are using static displays (Leds), 
    # we don't do anything here.
    # A connected LCD screen would require 
    # continuous updating

    if STATE == "Record":
        pass
    elif STATE == "Pause":
        pass
    elif STATE == "Stop":
        pass
    else:
        pass


main()


