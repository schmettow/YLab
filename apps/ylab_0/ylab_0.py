"""
YLab0: YEDA recorder
"""


import board
import time

from sensory import Yeda
from yui import Shortlong, RGB
from ydata import SDcard

print("YLab0 says hi!")
def main():
    STATE = "Init"
    print(STATE)

    yeda = Yeda()
    yeda.connect()

    SDcard.init()
    drive = SDcard(yeda, filename = "ylab0_" + str(time.time()) + ".csv")
    drive.connect()
    
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
                        break
                
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
            if yeda.sample():
                yeda.print()
                yeda.buffer()
            drive.update()
        elif STATE == "Pause":
            if yeda.sample():
                yeda.print()
        elif STATE == "Stop":
            pass
        else:
            pass


main()



