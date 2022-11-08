"""
testing the speed of reading a sensor
"""

from sensory import Yeda, this_moment

measures = []
hz = 1000
buffer = int(hz)

def reset_measures():
    global measures
    measures = []
    
def main():
    State = "Init"
    print(State)

    sensor = Yeda(sample_interval = 1/hz)
    sensor.connect()
    
    reset_measures()
    
    State = "Measure"
    print(State)
    
    now = this_moment()
    
    while True:
        if sensor.sample():
            last = now
            now = this_moment()
            if len(measures) == 0 or not len(measures) % hz == 0:
                measures.append(now - last)
            else:
                avg = sum(measures)/len(measures)
                print("hz_avg:", int(1/avg))
                reset_measures()
main()

## Assignment: Also print min and max.
