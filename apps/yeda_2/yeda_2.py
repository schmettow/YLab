"""
YEDA_2 improves on Yeda_1 by using libyeda (object-oriented)
"""


import board
import time

from libyeda import Yeda, this_moment
from libylab import Button, RGB

HZ = 10 ## sampling frequency in Hz
UPDATE = 1/HZ
PIN = board.GP27_A1
SAVE = 1
PRINT = False


print("YEDA 2")
def main():

    Yeda_0 = Yeda( pin = PIN,
                        update_interval = UPDATE,
                        save_interval = SAVE )
    try:
        Yeda_0.connect()
    except:
        print("Error: Could not connect Yeda_0.")
        exit()
    
    BT2 = Button(pin = board.GP21)
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
                        Yeda_0.reset_data()
                        STATE = "Record"
                    ## --> STOP
                elif BT2.event == "long":
                    STATE = "Stop"
                    #Yeda_0.save_data()
                
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
            if Yeda_0.sample():
                #Yeda_0.print()
                Yeda_0.record()
                #Yeda_0.save_data()
        elif STATE == "Pause":
            Yeda_0.sample()
            #Yeda_0.print()
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



