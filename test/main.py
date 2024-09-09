#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# This is a function that waits for a desired color.
def wait_for_color(desired_color):
    # While the color is not the desired color, we keep waiting.
    while sensor.color() != desired_color:
        wait(20)    


# Create your objects here.
ev3 = EV3Brick()
test_motor = Motor(Port.B)
sensor = ColorSensor(Port.S4)
ev3.speaker.beep()

# 
while True:
    print(sensor.color())
while sensor.color == Color.

# while sensor.color == Color.WHITE:
  #  test_motor.run_target(-500,90)

#print("Waiting for Yellow ...")
#wait_for_color(Color.YELLOW)
#print("Yellow found")


ev3.speaker.beep(1000,500)
# Write your program here.
ev3.speaker.beep()
