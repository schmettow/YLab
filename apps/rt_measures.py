"""
simple RT experiment, simulating a brake light
"""

from yui import Buzzer, RGB, this_moment
import random

def main():
    State = "Init" # "Wait" "Signal"
    print(State)

    signal = RGB()
    signal.connect()
    buzz = Buzzer()
    buzz.connect()
    
    
    due_signal = 2 # seconds
    due_response = 1
    timestamp = this_moment()
    rt = []
    State = "Wait"
    # print(State)
    
    while True:
        now = this_moment()
        if State == "Wait":
            if (now - timestamp) >= due_signal:
                signal.red()
                timestamp = now
                State = "Signal"
                # print(State)
        elif State == "Signal":
            if (now - timestamp) >= due_response:
                signal.dred()
                timestamp = now
                due_signal = random.randrange(2,4)
                State = "Wait"
                # print(State)
            if buzz.update():
                if buzz.value:
                    this_rt = buzz.time - timestamp
                    print("RT:", this_rt)
                    rt.append(this_rt)
                    signal.dred()
                    timestamp = now
                    State = "Wait"
main()
