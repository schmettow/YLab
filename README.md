# YLab is your Lab

[Getting started with YLab](https://schmettow.github.io/YLab/)

The goal of YLab is to create an educational platform to learn about physiological measure and sensors arrays.
The idea is to create a low budget software/hardw3are platform, that allows students to own their devices.

The platform can be used to teach students all about collecting, analysing and interpreting physiological data, like EDA or EMG. At the same time it offers a way to teach students programming in a fun and easy way.

YLab is based on a Raspberry Pico (not Pi), that sits on a Maker Pi board with additional components and Grove interfaces. The sensors are mainly from the Grove collection.

## Supported devices

In theory, all hardware supported by Circuitpython by Adafruit is capable of running YLab

### Boards

+ Cytron Maker Pi Pico

### Sensors

The package Sensory provides a consistent interface for sampling data from sensors. 
Currently, the following sensors are implemented.

+ all analog sensors (GSR, EMG, EEG)
+ ADS1115 via I2C (provides four analog inputs)
+ LIS3DHTR 3 dof acceleration sensor
+ DHT11 atmospheric temperature and humidity sensor
+ moment of interest coding via button presses
+ contact sensors, e.g. for implementing the buzz wire game

### User interface

The YUI package provides UI elements to creeate the user interface.
Currently the following devices are supported:

+ buttons, with various events, such as press or long press
+ RGB Led
+ Led
+ Buzzer

### Storage

The package Ydata provides various data storage mechanisms. 
Currently the following two are implemented:

+ writing CSV to an SDcard
+ writing CSV up the usb line

