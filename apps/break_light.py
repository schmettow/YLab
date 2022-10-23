"""
Controlling a brake light
"""

from yui import LED, Buzzer

def main():
    pedal = Buzzer()
    pedal.connect()
    brake_light = LED()
    brake_light.connect()
    brake_light.off()
    if pedal.value: brake_light.on()
    
    while True:
        if pedal.update():
            if pedal.value:
                brake_light.on()
            else:
                brake_light.off()
main()
