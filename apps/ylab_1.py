"""
YLab1(Ylab0): YEDA and Yema recorder
"""


import board
import time

from sensory import Yeda, Yema_ads, Sensory
from yui import Button, RGB
from ydata import SDcard

print("YLab0 says hi!")
def main():
    STATE = "Init"
    print(STATE)

    yeda = Yeda()
    yeda.connect()
    yema = Yema_ads()
    yema.connect()
    
    sensory = Sensory([yeda, yema])
        
    SDcard.init()
    drive = SDcard(sensory, filename = "ylab0_" + str(time.time()) + ".csv")
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
                        STATE = "Record"
                    ## --> STOP
                elif btn.event == "long":
                    if STATE == "Stop":
                        drive.disconnect()
                        rgb.off()
                        STATE = "End"
                        print("YLab0 says bye.")
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



