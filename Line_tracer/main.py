#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
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

STATES=["DRIVE","STOP","SLOW","TURN_LEFT","TURN_RIGHT","SWITCH_LANE","HOLD"]#All possible states the robot can have 
LANE_STATES=["UNKNOWN","LEFT_LANE","RIGHT_LANE"]
rounds=1
state=STATES[1]
lane_state=LANE_STATES[0]
Speed = 50

# Initialize the drive base.
robot = DriveBase(motor_left, motor_right, wheel_diameter=55, axle_track=145) #Check for correct Parameter 

def update_sensors(): #Update sensor readings
    color_left = sensor_left.color()
    color_right = sensor_right.color()
    return color_left, color_right

#function changes state depending of sensor outputs
def transition_state(color_left, color_right): 
    global state
    global lane_state
    global rounds

    if left_color == Color.BLACK and right_color == Color.BLACK:
        state=STATES[0] # Move forward

    if left_color == Color.GREEN:
        state=STATES[4]

    if right_color==Color.GREEN:
        state=STATES[3]

    if left_color == Color.BLACK and right_color == Color.WHITE:
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[1]
        state=STATES[3]

    if left_color == Color.WHITE and right_color == Color.BLACK:
        state=STATES[4]
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[2]
        
    if left_color == Color.YELLOW and right_color == Color.YELLOW:
        state=STATES[2]

    if left_color == Color.RED and right_color == Color.RED:
        if rounds<=0:
            state=STATES[1]
        state=STATES[5]
        
    if left_color == Color.BLUE and right_color == Color.BLUE:
        state=STATES[6]

    if left_color==None and right_color==None:
        state=STATES[1]
        lane_state==[0]


#Executes operations depending of the state 
def switch(state):  
    global rounds
    if state ==  "DRIVE":
        robot.drive(Speed,0)         
    elif state ==  "STOP":
        robot.drive(0,0)
    elif state ==  "SLOW":
        robot.drive(Speed/2,0)
    elif state ==  "TURN_LEFT":
        robot.drive(Speed,-45)
    elif state ==  "TURN_RIGHT":
        robot.drive(Speed,45)
    elif state ==  "SWITCH_LANE":
        if lane_state=="LEFT_LANE":
            robot.drive(Speed,45)
            wait(600)# timing needs to be relativ to the speed. (maybe wait(30000/speed)). 30000 is the distance
            robot.drive(Speed,0)
            wait(3000)
            robot.drive(Speed,-45)
            wait(600)
            robot.drive(Speed,0)
            rounds-=1
        elif lane_state=="RIGHT_LANE":
            robot.drive(Speed,-45)
            wait(600)
            robot.drive(Speed,0)
            wait(2000)
            robot.drive(Speed,45)
            wait(600)
            robot.drive(Speed,0)
            rounds-=1
    elif state == "HOLD":
        robot.drive(0,0)
        wait(3000)
        robot.drive(Speed,0)
        wait(1000)

    # match state:
    #     case "DRIVE":
    #         robot.drive(Speed,0)         
    #     case "STOP":
    #         robot.drive(0,0)
    #     case "SLOW":
    #         robot.drive(Speed/2,0)
    #     case "TURN_LEFT":
    #         robot.drive(Speed,-45)
    #     case "TURN_RIGHT":
    #         robot.drive(Speed,45)
    #     case "SWITCH_LANE":
    #         if lane_state=="LEFT_LANE":
    #             robot.drive(Speed,45)
    #             wait(600)
    #             robot.drive(Speed,0)
    #             wait(3000)
    #             robot.drive(Speed,-45)
    #             wait(600)
    #             robot.drive(Speed,0)
    #             rounds-=1
    #         elif lane_state=="RIGHT_LANE":
    #             robot.drive(Speed,-45)
    #             wait(600)
    #             robot.drive(Speed,0)
    #             wait(2000)
    #             robot.drive(Speed,45)
    #             wait(600)
    #             robot.drive(Speed,0)
    #             rounds-=1
    #     case "HOLD":
    #         robot.drive(0,0)
    #         wait(3000)
    #         robot.drive(Speed,0)
    #         wait(1000)

#main loop of the programm
while True:
    # Update sensor readings
    left_color, right_color = update_sensors()
    #print(left_color)
    
    # Handle state transitions
    wait(10)
    transition_state(left_color, right_color)
    switch(state)
    print(state)
    


# Write your program here.
ev3.speaker.beep()
