"""
testing the speed of reading a sensor
"""

from sensory import *
    
def main():
    State = "Init"
    print(State)
    
    #ads = ADS()
#     sensory = Sensory([Sensor_ads(ads, 0, sample_interval = 0),
#                        Sensor_ads(ads, 1, sample_interval = 0),
#                        Sensor_ads(ads, 2, sample_interval = 0),
#                        Sensor_ads(ads, 3, sample_interval = 0),
#                        Sensor_analog(sample_interval = 0)])

    sensory = Yxz_3D(sample_interval = 0)
    sensory.connect()
    
    n_measures = 0
    now = last = this_moment()
    time_since = 0
    
    State = "Measure"
    print(State)
    
    while True:
        if sensory.sample():
            n_measures = n_measures + 1
            
        now = this_moment()
        time_since = now - last
        if  time_since >= 1:
            hz = n_measures/time_since
            print("hz:", int(hz))
            n_measures = 0
            last = now
            sensory.reset_data()
main()

## Assignment: Also print min and max.
