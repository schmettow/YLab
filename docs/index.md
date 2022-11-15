# Getting started with YLab 0

1. Download YLab0.zip and unpack it
1. Connect the Maker Pi and wait until the drive window connects
1. Copy the YLab folder apps to the drive
1. Copy the content of YLab folder lib to the folder /lib on the drive
1. Insert a freshly as FAT32 formatted SD card into the slot on the Pi
1. Connect the Grove GSR kit to port 6
1. Download and install Thonny
1. Run Thonny and open Run: Select Interpreter
1. Select CircuitPython and connect to the serial port
1. Load apps/ylab_0.py into Thonny
1. Activate View: Plotter in Thonny
1. Hit the Run button

To run YLab0:

1. When the program starts, it is in Stop mode (White).
1. Clicking button GP20 enters Pause mode (Green), where the program samples the sensor and print results it to the screen. You should see numbers printed to teh console and a moving graph in Plotter
1. Clicking the button again activates Record mode (Red), where the sampled data is collected and regularly transferred from the sensor to a file on the SD card. You should see the leds GP10 - GP13 flicker every second
1. Shortlong 20 toggles between Record and pause mode
1. A long press on the button enters Stop mode (White).
1. In Stop mode a long press ends YLab0

The results of recordings are stored as a file ylab0_<seconds>.csv on the SDcard. 
To use it, remove the SDcard and put it into a slot on your computer (you may need a microSD adaptor).
The CSV files can be opened with any data analysis system.

The data is stored in the YLab very long format, where every atomic measure occupies one row,
together with a time stamp and the sensor ID. A useful plot in R can be produced as follows:

ylab_data |>
    ggplot(aes(x = time, y = value)) +
    geom_line()

If you want to use YLab0 on-the-go:

1. copy apps/ylab_0.py to / and rename the file to code.py
1. connect the Ylab system to a USB powerbank and run

