"""
YLab1(Ylab0): YEDA, Yema and Event recorder
"""

print("YLab0 says hi!")

import board
import time

from sensory import Yeda, Yema_ads, MOI, Sensory
from yui import Button, RGB
from ydata import SDcard

def main():
    STATE = "Init"
    print(STATE)

    yeda = Yeda()
    yeda.connect()
    yema = Yema_ads()
    yema.connect()
    
    marker_1 = MOI()
    marker_1.pins = board.GP21
    marker_1.connect()
    marker_2 = MOI()
    marker_1.pins = board.GP22
    marker_2.connect()
    
    sensory = Sensory([yeda, yema, marker_1, marker_2])
    #sensory.connect()
        
    SDcard.init()
    drive = SDcard(sensory, filename = "ylab1_" + str(time.time()) + ".csv")
    drive.connect()
    
    btn = Button()
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
                    ## Init --> Pause
                    if STATE == "Init":
                        STATE = "Pause"
                    ## Record --> Pause
                    elif STATE == "Record":
                        STATE = "Pause"
                    ## Pause --> Record
                    elif STATE == "Pause":
                        STATE = "Record"
                    ## Stop --> Record
                    elif STATE == "Stop":
                        yeda.reset_data()
                        drive.filename = "ylab1_" + str(time.time()) + ".csv"
                        STATE = "Record"
                    ## --> STOP
                elif btn.event == "long":
                    if STATE == "Stop":
                        drive.disconnect()
                        rgb.off()
                        STATE = "End"
                        print("YLab0 says bye.")
                        break
                    else:
                        STATE = "Stop"
                        drive.write()
                
                ## Updating the static displays ##
                if STATE == "Record":
                    rgb.red()
                elif STATE == "Pause":
                    rgb.green()
                elif STATE == "Stop":
                    rgb.white()
                
                print(STATE)
            

        ################ Continuous processing #############

        if STATE == "Record":
            if sensory.sample():
                sensory.print()
                sensory.record()
            drive.update()
        elif STATE == "Pause":
            if sensory.sample():
                sensory.print()
        elif STATE == "Stop":
            pass
        else:
            pass


main()



