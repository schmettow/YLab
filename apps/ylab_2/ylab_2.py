"""
YLab1(Ylab0): YEDA and MOI
"""


import board
import time

from sensory import Sensor_analog, Sensor_ads, MOI, Sensory, ADS
from yui import Button, RGB
from ydata import SDcard

def main():
    STATE = "Init"
    print(STATE)
    
    ads = ADS(gain = 8)
    
    sensory = Sensory([MOI(pins = board.GP21),
                       MOI(pins = board.GP22),
                       Sensor_analog(sample_interval = 1/100), # yema
                       Sensor_ads(ads, 0, sample_interval = 1/20)])
    sensory.connect()
        
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
                        sensory.reset_data()
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



