#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color # type: ignore
from pybricks.iodevices import Ev3devSensor
from pybricks.tools import print, wait, StopWatch

# calibrating colours
color_sensor = Ev3devSensor(Port.S4)

while True:
    r, g, b = color_sensor.read('RGB-RAW')
    # Print results
    print('R: {0}\t G: {1}\t B: {2}'.format(r, g, b))
    wait(1000)