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

# Set-up functions
ev3 = EV3Brick()
motor_left = Motor(Port.C)
motor_right = Motor(Port.B)
sensor_right = ColorSensor(Port.S4)
sensor_left = ColorSensor(Port.S3)
car = DriveBase(motor_left, motor_right, wheel_diameter=55.5, axle_track=104)
SPEED = 50


while True:
    car.drive(SPEED,0)    

    if sensor_left.color() == Color.GREEN and sensor_right.color() == Color.BLACK: # turn right
        print ("turn right")
        car.turn(20)
    if sensor_right.color() == Color.GREEN and sensor_left.color() == Color.BLACK: # turn left
        print ("turn left")
        car.turn(-20)
    if sensor_left.color() == Color.WHITE and sensor_right.color() == Color.BLACK: # turn left and go straight again
        car.turn(-10)
        print ("white sensored")
    if sensor_left.color() == Color.BLACK and sensor_right.color() == Color.WHITE: # turn right and go straight again
        car.turn(10)
        print ("white sensored")
    if sensor_left.color() == Color.BLUE or sensor_right.color() == Color.BLUE: # stop and go again
        print("wait for 3 seconds and go again")
        car.drive(0, 0)
        wait(3000) # wait for 3 sec (in miliseconds)
        car.drive(SPEED, 0)
    if sensor_left.color() == Color.YELLOW or sensor_right.color() == Color.YELLOW: # go half speed
        print("go half speed")
        for x in range(10): # for 10 seconds go half speed
            car.drive(SPEED/2, 0)
    if sensor_left.color() == Color.RED or sensor_right.color() == Color.RED:
        print("red sensored")
        # change lanes

# Write your program here.
# ev3.speaker.beep()
