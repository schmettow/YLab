import board
import time
import pwmio
import digitalio
from analogio import AnalogIn
from neopixel_write import neopixel_write

DEBUG = True

STATE = "Init"
print(STATE)

## Pico onboard LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

## Maker Pi onboard RGB led
rgb_pin = board.GP28
RGB = digitalio.DigitalInOut(rgb_pin)
RGB.direction = digitalio.Direction.OUTPUT

white = bytearray([10, 10, 10])
red = bytearray([0, 10, 0])
green = bytearray([5, 0, 0])

## Maker Pi onboard button
bt1_pin = board.GP20
BT1 = digitalio.DigitalInOut(bt1_pin)
BT1.switch_to_input(pull=digitalio.Pull.DOWN)

## Grove GSR sensor connected to Maker Pi Grove 6
## using onboard ADC
yeda_pin = board.GP27_A1
YEDA = AnalogIn(yeda_pin)

print("YEDA1")

def store_data():
    pass

def main():

    ## Initial state
    STATE = "Stop"
    led.value = False
    neopixel_write(RGB, white)

    ## Collecting data as list of tuples
    OUT = []

    ## Creating button Events
    this_bt1 = not BT1.value # getting state of button
    EventTime = 0
    EventType = ""
    print(STATE)

    ## Fast while loop
    while True:
        time.sleep(0.1)  ## go not so fast
        now = time.monotonic()  ## this time

        ############### Collecting button events ########

        ## Asking the current state of the button
        last_bt1 = this_bt1
        this_bt1 = not BT1.value
        ## Mark event on button state change
        Event = this_bt1 != last_bt1

        ################ Creating interaction events ############
        if Event:
            ## remembering the last event
            lastEventTime = EventTime
            lastEventType = EventType
            EventTime = now

            if not this_bt1: ## released
                if (EventTime - lastEventTime) < 2: ## short release
                    EventType = "BT1_release"
                else:
                    EventType = "BT1_longrel" ## long release
            else:
                EventType = "BT1_pressed"
            last_bt1 = this_bt1  # and round it goes

        ################ Interactive transitionals #############

        if Event:
            if EventType == "BT1_release":
                ## Stop --> Record
                if STATE == "Stop" or STATE == "Pause":
                    STATE = "Record"
                    led.value = True
                    neopixel_write(RGB, red)
                ## Record --> Pause
                elif STATE == "Record":
                    STATE = "Pause"
                    led.value = False
                    neopixel_write(RGB, green)
            elif EventType == "BT1_longrel":
                STATE = "Stop"
                led.value = False
                neopixel_write(RGB, white)
            elif EventType == "BT1_pressed":
                pass
            print(STATE)

        ################ Data collection #####################

        if STATE == "Record":
            this_eda = YEDA.value / 65536  ## take measure
            # OUT.append((now, this_eda)) ## careful with limited memory
            print((this_eda,))  ## best viewed in a serial plotter

main()

