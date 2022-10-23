"""
Automatic traffic light
"""


import time
from yui import RGB, Buzzer, this_moment

def main():
    State = "Init" # "Drive", "Warn", "Stop"
    print(State)
    due_warn, due_stop, due_drive = (3, 1, 1)
    signal = RGB()
    signal.connect()

    t_last_event = this_moment()
    signal.green()
    State = "Drive"


    while True:
        now = this_moment()
        
        if State == "Drive":
            if (now - t_last_event) >= due_warn:
                t_last_event = now
                signal.yellow()
                State = "Warn"
                print(State)
        elif State == "Warn":
            if (now - t_last_event) >= due_stop:
                t_last_event = now
                signal.red()
                State = "Stop"
                print(State)
        elif State == "Stop":
            if (now - t_last_event) >= due_drive:
                t_last_event = now
                signal.green()
                State = "Drive"
        else:
            print("Unexpected state: shutting down")
            break # stopping the fast loop    
    return False

main()