"""
Manual traffic light
"""


import time
from yui import RGB, Buzzer, this_moment

def main():
    State = "Init" # "Drive", "Warn", "Stop"
    print(State)
    signal = RGB()
    signal.connect()
    
    button = Buzzer()
    button.connect()
    
    signal.green()
    State = "Drive"


    while True:
        if button.update():
            if button.value:
                if State == "Drive":
                    signal.yellow()
                    State = "Warn"
                    print(State)
                elif State == "Warn":
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
    return False

main()