import board
import time
import pwmio
import digitalio
from analogio import AnalogIn
from neopixel_write import neopixel_write

DEBUG = True
tick = 0.01 ## 10 ms

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
red   = bytearray([0, 10, 0])
green = bytearray([5, 0, 0])
blue  = bytearray([0, 0, 3])

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
    this_BT1 = not BT1.value ## default state is closed
    led.value = False
    neopixel_write(RGB, white)

    ## Collecting data as list of tuples
    OUT = []

    ## Creating initial button Events
    print(STATE)
    
    ## Preparing event handling
    ## Mark event on button state change
    event_time = 0
    event_type = ""

    
    ## Fast while loop
    while True:
        ## This is far from perfect, because
        ##  the ticks also influence the responsiveness of the interface
        ## Still, analogue sensors update continuously and we have to slow it down just a bit
        time.sleep(tick)  
        now = time.monotonic()  ## this time



        ############### Collecting button events ########

        ## Note that buttons are not like switches, as they bounce back.
        ## What matters is to discover state changes and create higher-level
        ## events. 
        ## What matters first is to discover when the button changes its state
        
        last_BT1 = this_BT1
        this_BT1 = not BT1.value # to press means to disrupt the circuit
        Event = this_BT1 != last_BT1

        ################ Creating interaction events ############
        ## Now the button event is classified further.
        ## By time stamps we can create more advanced interaction modes
                
        if Event:
            ## remembering the last event time
            last_event_time = event_time
            event_time = now
            
            if not this_BT1: ## released after short or long press
                if (event_time - last_event_time) < 1: ## short release
                    event_type = "BT1_short"
                else:
                    event_type = "BT1_long" ## long release
            else:
                event_type = "BT1_press"
            # print(event_type)

        ################ Interactive transitionals #############

        
        if Event:
            if event_type == "BT1_short":
                ## Stop --> Record
                if STATE == "Record":
                    STATE = "Pause"
                    led.value = False
                    neopixel_write(RGB, green)
                elif STATE == "Stop" or STATE == "Pause":
                    STATE = "Record"
                    led.value = True
                    neopixel_write(RGB, red)
                ## Record --> Pause
            elif event_type == "BT1_long":
                STATE = "Stop"
                led.value = False
                neopixel_write(RGB, white)
            # print(STATE) if DEBUG



        ################ Continuous display #############

        if STATE == "Record":
            pass
        elif STATE == "Pause":
            pass
        elif STATE == "Stop":
            pass
        else:
            pass

        ################ Data collection #####################

        if STATE == "Record":
            this_eda = YEDA.value / 65536  ## take measure
            # OUT.append((now, this_eda)) ## careful with limited memory
            print((this_eda,))  ## best viewed in a serial plotter

main()



