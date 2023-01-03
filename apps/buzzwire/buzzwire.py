"""
YLab: Buzzwire task with one buzz contact and one base station contact, plus Yema and Yxz
"""

import board
import time

from sensory import Sensory, Contact, MOI, Yxz_3D, Yema
from yui import Shortlong, RGB, Buzz
from ydata import SDcard

def main():
    wire = Contact(ID = "buzz",
                   pins = board.GP0,
                   sample_interval = 1/100)   ## Grove 1
    station = Contact(ID = "station", pins = board.GP1) ## Grove 1
    sensory = Sensory( [wire,
                        station,
                        MOI(pins = board.GP21, ID = "start"),
                        MOI(pins = board.GP22, ID = "stop"),
                        Yema(sample_interval = 0.1),
                        Yxz_3D(sample_interval = 0.1)] )
    sensory.connect()
    
    SDcard.init()
    drive = SDcard(sensory,
                   filename = "ylab_buzzwire" + str(time.time()) + ".csv")
    drive.save_interval = 5
    drive.connect()
    
    btn = Shortlong()
    btn.connect()
    
    rgb = RGB()
    rgb.connect()
    
    buzzer = Buzz() ## used as continuous feedback
    buzzer.connect()
    
    
    State = "Stop"
    rgb.white()
    buzzer.off()
        
    ## Fast while loop
    while True:
        ################ Interactive transitionals #############
        if btn.update():
            if btn.update_event():
                if btn.event == "short":
                    ## Init --> Pause
                    if State == "Init":
                        rgb.green()
                        State = "Pause"
                    ## Record --> Pause
                    elif State == "Record":
                        rgb.green()
                        State = "Pause"
                    ## Pause --> Record
                    elif State == "Pause":
                        rgb.red()
                        State = "Record"
                    ## Stop --> Record
                    elif State == "Stop":
                        rgb.red()
                        sensory.reset_data()
                        drive.filename = "ylab1_" + str(time.time()) + ".csv"
                        State = "Record"
                    ## --> STOP
                elif btn.event == "long":
                    if State == "Stop":
                        drive.disconnect()
                        rgb.off()
                        State = "End"
                        print("YLab0 says bye.")
                        break
                    else:
                        rgb.white()
                        buzzer.off()
                        State = "Stop"
                
                # print(State)
            

        ################ Continuous processing #############

        if State == "Record":
            if sensory.sample():
                sensory.print()
                sensory.record()
                buzzer.switch(wire.value)
            drive.update()
        elif State == "Pause":
            if sensory.sample():
                sensory.print()
                buzzer.switch(wire.value)
        elif State == "Stop":
            pass
        else:
            pass

main()



