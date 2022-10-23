import time
from yui import RGB, Buzzer, this_moment

def main():
    State = "Init" # "OK", "Warn", "Alarm"
    print(State)
    due_warn, due_alarm, due_shutdown = (2, 1, 1)
    switch = Buzzer()
    switch.connect()
    signal = RGB()
    signal.connect()
    signal.white()
    t_last_event = this_moment()
    
    State = "OK"


    while True:
        now = this_moment()
        
        if switch.update():
            signal.green()
            t_last_event = now
            State = "OK"
            print(State)

        if State == "OK":
            if (now - t_last_event) >= due_warn:
                t_last_event = now
                signal.red()
                State = "Warn"
                print(State)
        
        if State == "Warn":
            if (now - t_last_event) >= due_alarm:
                t_last_event = now
                signal.white()
                State = "Alarm"
                print(State)
        
        if State == "Alarm":
            if (now - t_last_event) >= due_shutdown:
                signal.off()
                break # stopping the fast loop    
    return False

if not main(): print("Operator overdue. Shutting down!")
