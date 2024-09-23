#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color # type: ignore
from pybricks.iodevices import Ev3devSensor
from pybricks.tools import print, wait, StopWatch
# Create your objects here.
ev3 = EV3Brick()

Color.GREEN = Color(h=132, s=94, v=26)
Color.YELLOW = Color(h=348, s=96, v=40)
Color.WHITE = Color(h=17, s=78, v=15)
Color.BLACK = Color(h=17, s=78, v=15)
Color.RED = Color(h=359, s=97, v=39)
# Calibrated list of colors saved
cal_colors = (Color.GREEN, Color.YELLOW, Color.WHITE, Color.BLACK, Color.RED, Color.NONE)
sensor_left.detectable_colors(cal_colors)
sensor_right.detectable_colors(cal_colors)

# calibrating colours
color_sensor = Ev3devSensor(Port.S4)

while True:
    if ev3.buttons.pressed() == True:
        print ("pressed")
    r, g, b = color_sensor.read('RGB-RAW')
    # Print results
    print('R: {0}\t G: {1}\t B: {2}'.format(r, g, b))
    wait(1000)

    