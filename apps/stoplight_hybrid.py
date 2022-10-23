"""
Hybrid traffic light
"""


import time
from yui import RGB, Buzzer, this_moment

def main():
    State = "Init" # "Drive", "Warn", "Stop"
    print(State)
    signal = RGB()
    signal.connect()
    due_stop = 1 # seconds
    
    button = Buzzer()
    button.connect()
    
    signal.green()
    State = "Drive"

    while True:
        now = this_moment()
        if button.update() and button.value:
            if State == "Drive":
                signal.yellow()
                t_enter_warn = now # <-- timestamp
                State = "Warn"
                print(State)
            elif State == "Warn": # always leave the user in control
                signal.red()
                State = "Stop"
                print(State)
            elif State == "Stop":
                signal.green()
                State = "Drive"
            else:
                print("Unexpected state: shutting down")
                signal.off()
                break # stopping the fast loop
        
        if State == "Warn" and (now - t_enter_warn) >= due_stop:
            signal.red()
            State = "Stop"
            print(State)
        
    return False

main()