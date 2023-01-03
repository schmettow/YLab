"""
YLab: Buzzwire task with one buzz contact and one base station contact, plus Yema and Yxz
"""

import board
import time

from sensory import Sensory, ContactEvent, MOI, Yxz_3D, Yema, DHT11
from yui import Shortlong, RGB, Buzz
from ydata import SDcard

def make_filename():
    return "ylab_buzzwire" + str(time.time()) + ".csv"

def main():
    wire = ContactEvent(ID = "buzz",
                   pins = board.GP0,
                   sample_interval = 1/100)   ## Grove 1
    station = ContactEvent(ID = "station", pins = board.GP1) ## Grove 1
    sensory = Sensory( [wire,
                        station,
                        MOI(pins = board.GP21, ID = "start"),
                        MOI(pins = board.GP22, ID = "stop"),
                        DHT11(),
                        Yema(sample_interval = 0.1),
                        Yxz_3D(sample_interval = 0.1)] )
    sensory.connect()
    
    SDcard.init()
    drive = SDcard(sensory,
                   filename = make_filename())
    drive.save_interval = 5
    
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
                # short press
                if btn.event == "short":
                    ## Init --> Pause
                    if State == "Init":
                        rgb.green()
                        drive.connect()
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
                        drive.filename = make_filename()
                        drive.connect()
                        State = "Record"
                # long press
                elif btn.event == "long":
                    ## --> STOP
                    if not State == "Stop":
                        drive.disconnect()
                        rgb.white()
                        buzzer.off()
                        State = "Stop"
                    ## --> END
                    else:
                        SDcard.final()
                        rgb.off()
                        State = "End"
                        print("Buzzwire says bye.")
                        break
                        
                
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



