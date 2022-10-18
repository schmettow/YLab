"""
YEDA_2 improves on Yeda_1 by using libyeda (object-oriented)
"""


import board
import time
# import pwmio
import digitalio
# from analogio import AnalogIn
from neopixel_write import neopixel_write

import libyeda as yeda

HZ = 10 ## sampling frequency in Hz
UPDATE = 1/HZ
PIN = board.GP27_A1
SAVE = 1
PRINT = False


print("YEDA 2")

def main():

    Yeda_0 = yeda.Yeda( pin = PIN,
                        update_interval = UPDATE,
                        save_interval = SAVE )
    try:
        Yeda_0.connect()
    except:
        print("Error: Could not connect Yeda_0.")
        exit()

    
    ## Initial state
    this_BT1 = not BT1.value ## default button state is closed
    Led.value = False # display
    neopixel_write(RGB, white)
    event_time = 0 ## event handling
    event_type = "" ## 

    STATE = "Stop"
    print(STATE)
    
    
    ## Fast while loop
    while True:
        now = time.monotonic()  ## this time
        ############### Collecting button state changes ########

        ## Note that buttons are not like switches. They bounce back.
        ## What matters is to discover state changes and create higher-level
        ## events. 
        ## What matters first is to discover when the button changes its state
        
        last_BT1 = this_BT1
        this_BT1 = not BT1.value # to press means to disrupt the circuit
        Event = this_BT1 != last_BT1

        ################ Creating button events ############
        ## Now the button event is classified further.
        ## By time stamps we can create more advanced interaction modes
                
        if Event:
            ## remembering the last event time
            last_event_time = event_time
            event_time = now
            
            if not this_BT1: ## released after short or long press
                if (event_time - last_event_time) < 1: ## short release
                    event_type = "BT1_short"
                else:
                    event_type = "BT1_long" ## long release
            else:
                event_type = "BT1_press"
            # print(event_type)

        ################ Interactive transitionals #############


        # Note that RGB is static. You write a value and it stays. 
        # No need to create presentitionals. The order of the 
        # inner  conditions is completely arbitrary. The order is entirely
        # determined by transitions.
        
        if Event:
            if event_type == "BT1_short":
                ## Record --> Pause
                if STATE == "Record":
                    neopixel_write(RGB, green)
                    STATE = "Pause"
                ## Pause --> Record
                elif STATE == "Pause":
                    neopixel_write(RGB, red)
                    STATE = "Record"
                ## Stop --> Record
                elif STATE == "Stop":
                    neopixel_write(RGB, red)
                    Yeda_0.reset_data()
                    STATE = "Record"
                ## --> STOP
            elif event_type == "BT1_long":
                STATE = "Stop"
                neopixel_write(RGB, white)
                Yeda_0.save_data()
            print(STATE)
            

        ################ Continuous processing #############

        if STATE == "Record":
            if Yeda_0.update():
                Yeda_0.print()
                Yeda_0.record()
                Led.value = True ## This mimicks a hard drive LED
                Yeda_0.save_data()
                Led.value = False
        elif STATE == "Pause":
            Yeda_0.update()
            Yeda_0.print()
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



def setup():
    global Led, RGB, BT1, green ,red, white, blue, board

    ## Pico onboard LED
    Led = digitalio.DigitalInOut(board.LED)
    Led.direction = digitalio.Direction.OUTPUT

    ## Maker Pi onboard RGB led
    rgb_pin = board.GP28
    RGB = digitalio.DigitalInOut(rgb_pin)
    RGB.direction = digitalio.Direction.OUTPUT

    white = bytearray([10, 10, 10])
    red   = bytearray([0, 10, 0])
    green = bytearray([5, 0, 0])
    blue  = bytearray([0, 0, 3])

    ## Maker Pi onboard button
    bt1_pin = board.GP20
    BT1 = digitalio.DigitalInOut(bt1_pin)
    BT1.switch_to_input(pull=digitalio.Pull.DOWN)


setup()
main()



