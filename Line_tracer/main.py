#!/usr/bin/env pybricks-micropython
from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color # type: ignore
from pybricks.iodevices import Ev3devSensor
from pybricks.tools import print, wait, StopWatch

# calibrating colours
color_sensor = Ev3devSensor(Port.S4)
# color_sensor  = ColorSens_or(Port.S4)

def rgb_to_hsv(rgb):
    hsv = [0, 0, 0]
    normRgb = [0, 0, 0]

    for i in range(3):
      normRgb[i] = rgb[i] / 100

    cMax = max(normRgb)
    cMin = min(normRgb)
    diff = cMax - cMin

    if cMax == cMin:
      hsv[0] = 0
    elif cMax == normRgb[0]:
      hsv[0] = 60 * (normRgb[1] - normRgb[2]) / diff
    elif cMax == normRgb[1]:
      hsv[0] = 60 * (2 + (normRgb[2] - normRgb[0]) / diff)
    else:
      hsv[0] = 60 * (4 + (normRgb[0] - normRgb[1]) / diff)

    if hsv[0] < 0:
      hsv[0] += 360

    if cMax == 0:
      hsv[1] = 0
    else:
      hsv[1] = diff / cMax * 100

    hsv[2] = cMax * 100

    return hsv
while True:
    h, s, v = rgb_to_hsv(color_sensor.read('RGB-RAW'))
    print('H: {0}\t S: {1}\t V: {2}'.format(h, s, v))
    # r, g, b = color_sensor.read('RGB-RAW')
    
    # # Print results
    # print('R: {0}\t G: {1}\t B: {2}'.format(r, g, b))

    wait(1000)
