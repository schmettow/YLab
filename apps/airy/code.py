"""
YLab Air: Respiration tracking with CO2 and EMG
"""


import board
import time

from sensory import Yema, Scd41, MOI, Sensory
from yui import Shortlong, RGB
from ydata import BSU

print("YLab Air says hi!")
def main():
    STATE = "Init"
    print(STATE)

    yema = Yema()
    airy = Scd41()
    moi_in = MOI(pins = board.GP21)
    moi_ex = MOI(pins = board.GP22)
    sensory = Sensory([yema, airy, moi_in, moi_ex])
    sensory.connect()
    
    usb = BSU(sensory)
    
    btn = Shortlong()
    btn.connect()
    
    rgb = RGB()
    rgb.connect()
    rgb.white()
        
    ## Fast while loop
    while True:
        ################ Interactive transitionals #############
        if btn.update():
            if btn.update_event():
                if btn.event == "short":
                    ## Init --> Active
                    if STATE == "Init":
                        STATE = "Active"
                    ## Record --> Active
                    elif STATE == "Record":
                        STATE = "Active"
                    ## Active --> Record
                    elif STATE == "Active":
                        STATE = "Record"
                    ## Stop --> Record
                    elif STATE == "Stop":
                        yema.reset_data()
                        STATE = "Active"
                    ## --> STOP
                elif btn.event == "long":
                    if STATE == "Stop":
                        STATE = "Record"
                        print("Next recording")
                    else:
                        STATE = "Stop"
                        BSU.update()
                
                ## Updating the static displays ##
                if STATE == "Record":
                    rgb.red()
                elif STATE == "Active":
                    rgb.green()
                elif STATE == "Stop":
                    rgb.white()
                
                print(STATE)
            

        ################ Continuous processing #############

        if STATE == "Record":
            if sensory.sample():
                usb.update()
        elif STATE == "Active":
            if sensory.sample():
                sensory.print()
        elif STATE == "Stop":
            pass
        else:
            pass


main()



