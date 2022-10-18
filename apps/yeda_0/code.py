import board
import time
import digitalio
from analogio import AnalogIn

tick = 0.5

## Pico onboard LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

## Maker Pi onboard button
BT1_pin = board.GP20
BT1 = digitalio.DigitalInOut(BT1_pin)
BT1.switch_to_input(pull=digitalio.Pull.DOWN)

## Grove GSR sensor connected to Maker Pi Grove 6
## using onboard ADC
yeda_pin = board.GP27_A1
YEDA = AnalogIn(yeda_pin)

print("YEDA0")

def main():

    ## Initial state
    STATE = "Pause"
    led.value = False

    ## Collecting data as list of tuples
    OUT = []

    ## Creating button Events
    last_BT1 = not BT1.value # getting initial state of button

    ##### Initial State
    STATE = "Pause"

    ## Fast while loop
    while True:
        time.sleep(tick)  ## go not so fast
        now = time.monotonic()  ## this time

        ############### Detecting button events ########
        this_BT1 = not BT1.value
        BT1_pressed = this_BT1 and not last_BT1

        ################ Interactive transitionals #############
        if BT1_pressed:
            ## Stop --> Record
            if STATE == "Pause":
                STATE = "Record"
                led.value = True
            ## Record --> Pause
            elif STATE == "Record":
                STATE = "Pause"
                led.value = False
            print(STATE)

        ################ Data collection #####################

        if STATE == "Record":
            this_eda = YEDA.value / 65536  ## take measure
            # OUT.append((now, this_eda)) ## careful with limited memory
            print((this_eda,))  ## best viewed in a serial plotter

main()
