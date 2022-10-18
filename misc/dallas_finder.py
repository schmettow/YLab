# Test and Demo code for Maker Pi Pico
# Reference: https://my.cytron.io/p-maker-pi-pico
# Installing CircuitPython - https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython
# Audio track credit: jeremy80 - L-R Tone Level Test @ -6 db max w/3 Sec. Countdown Leader
# Audio track reference: https://freesound.org/people/jeremy80/sounds/230639/

import board
import digitalio
import busio as io
import adafruit_ssd1306
import adafruit_ds18x20
from adafruit_onewire.bus import OneWireBus
from time import sleep

sensors = ["Dummy_1", "Dummy_2"]

def main():
    P_STATE = ""
    STATE = "Init"
    print("Dallas Finder")

    
    while True:
        if STATE == "Init":
            initialize_OLED()
            P_STATE = STATE
            STATE = "Scan"
        elif STATE == "Scan":
            initialize_sensor()
            line = 1
            for device in sensors:
                print(format_addr(device))
                addr = device.rom
                #oled.fill(0)
                oled.text(format_addr(device), 0, (line - 1) * 150, line)
                oled.show()
                line = line + 1
        elif STATE == "Read":
            read_sensors()
            oled.fill(0)
            oled.text(addr_fmt, 0, 0, 1)
            oled.text(str(temp), 0, 10, 2)
            oled.show()
        sleep(.01)
    

def initialize_OLED():
    global I2C
    try:
        global i2c
        i2c = io.I2C(board.GP7, board.GP6)
        global oled
        oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
        oled.fill(0)
        I2C = True
        print("I2C Init complete")
    except:
        print("I2C init failed")
        I2C = False

def initialize_sensor():
    global ow_bus
    global sensors
    try:
        ow_bus = OneWireBus(board.GP4)
        sensors = ow_bus.scan()
    except:
        print("OneWire Init failed")

    
def read_sensors():
    global temp
    global addr
    global addr_fmt
    for device in sensors:
        ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, device)
        temp = ds18b20.temperature
        print(addr_fmt(device))
        print(temp)
        
def format_addr(device):
    return " ".join([hex(i).replace("0x", "") for i in device.rom])
    
        

main()
