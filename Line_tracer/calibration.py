#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.iodevices import Ev3devSensor
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color # type: ignore
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile



# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Initialize the motors and sensors.
motor_left = Motor(Port.C) #Check for correct Port 
motor_right = Motor(Port.B) 
sensor_left= ColorSensor(Port.S3)
sensor_right= ColorSensor(Port.S4)

# Used for calibration
# Color.GREEN = Color(h=132, s=94, v=26)
# Color.YELLOW = Color(h=348, s=96, v=40)
# Color.WHITE = Color(h=17, s=78, v=15)
# Color.BLACK = Color(h=17, s=78, v=15)
# Color.RED = Color(h=359, s=97, v=39)
# Calibrated list of colors saved
# cal_colors = (Color.GREEN, Color.YELLOW, Color.WHITE, Color.BLACK, Color.RED, Color.NONE)
# sensor_left.detectable_colors(cal_colors)
# sensor_right.detectable_colors(cal_colors)


# Used for calibration
# color = sensor_left.hsv()
while True:
    color = sensor_left.hsv()
    print (color)
    wait(600)
