#!/usr/bin/env pybricks-micropython
import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color # type: ignore
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from collections import *
#from collections import counter



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
Speed = 200

left_array=deque([0])
right_array=deque([0])

# Initialize the drive base.
robot = DriveBase(motor_left, motor_right, wheel_diameter=55, axle_track=145) #Check for correct Parameter 

def update_sensors(): #Update sensor readings
    global left_array
    global right_array
    color_left = sensor_left.color()
    color_right = sensor_right.color()
    left_array.append(color_num(color_left))
    right_array.append(color_num(color_right))
    if len(left_array)>9:
        left_array.popleft()
    if len(right_array)>9:
        right_array.popleft()
    #print(right_array)
    color_left=most_common(left_array)
    color_right=most_common(right_array)

    return color_left, color_right

def most_common (array):
    count_dict={}

    for num in array:
        if num in count_dict:
         count_dict[num] += 1
        else:
            count_dict[num] = 1

    most_common_number = None
    max_count = 0

    for num, count in count_dict.items():
        if count > max_count:
            max_count = count
            most_common_number = num    
    
    #print(most_common_number)
    return most_common_number
   

 
#function changes state depending of sensor outputs
def transition_state(color_left, color_right): 
    global state
    global lane_state
    global rounds

    if left_color == 1 and right_color == 1:
        state=STATES[0] # Move forward

    if left_color == 2:
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[1]
        state=STATES[4]

    if right_color==2:
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[2]
        state=STATES[3]

    if left_color == 1 and right_color == 3:
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[1]
        state=STATES[3]

    if left_color == 3 and right_color == 1:
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[2]
        state=STATES[4]
        
    if left_color == 6 and right_color == 6: #slow down 
        state=STATES[2]
   
    if left_color == 4 and right_color == 4: #lane switch
        print("before")
        print(rounds)
        if rounds<1:
            state=STATES[1]
            print(rounds)
        else:
            state=STATES[5]
           # print(rounds)
        
    if left_color == 5 and right_color == 5: #3 sec stop
        state=STATES[6]

    if left_color==0 and right_color==0:
        state=STATES[1]
        lane_state=LANE_STATES[0]
        rounds=1


def color_num(color):
    if color ==None:
        return 0
    elif color== Color.BLACK:
        return 1
    elif color== Color.GREEN:
        return 2
    elif color== Color.WHITE:
        return 3
    elif color== Color.RED:
        return 4
    elif color == Color.BLUE:
        return 5
    elif color == Color.YELLOW:
        return 6
    else: 
        return 0


#Executes operations depending of the state 
def switch(state):  
    global rounds
    global Speed
    if state ==  "DRIVE":
        robot.drive(Speed,0)         
    elif state ==  "STOP":
        robot.drive(0,0)
    elif state ==  "SLOW":
        robot.drive(Speed/2,0)
        clear_array()
        wait(300000/Speed)
    elif state ==  "TURN_LEFT":
        robot.drive(Speed,-45)
        
    elif state ==  "TURN_RIGHT":
        robot.drive(Speed,45)
         
    elif state ==  "SWITCH_LANE":
        if lane_state=="LEFT_LANE":
            Speed=100
            robot.drive(Speed,45)
            wait(30000/Speed)# timing needs to be relativ to the speed. (maybe wait(30000/speed)). 30000 is the distance
            robot.drive(Speed,0)
            wait(200000/Speed)
            #robot.drive(Speed,-45)
            #wait(30000/Speed)
            #robot.drive(Speed,0)
            rounds=rounds-1
            clear_lane()
            clear_array()
            Speed=200
           # print(rounds)
        elif lane_state=="RIGHT_LANE":
            Speed=100
            robot.drive(Speed,-45)
            wait(30000/Speed)
            robot.drive(Speed,0)
            wait(200000/Speed)
           # robot.drive(Speed,45)
            #wait(30000/Speed)
            #robot.drive(Speed,0)
            rounds=rounds-1
            clear_lane()
            clear_array()
            Speed=200
            #print(rounds)
        else:
         
            print("No lane detected")
            robot.drive(Speed,45)
        clear_array()
    elif state == "HOLD":
        robot.drive(0,0)
        wait(3000)
        robot.drive(Speed,0)
        clear_array()
        wait(1000)

def clear_array():
    global left_array
    global right_array
    left_array=deque([])
    right_array=deque([])

def clear_lane():
    lane_state=LANE_STATES[0]

#main loop of the programm
while True:
    start=time.time()
    # Update sensor readings
    left_color, right_color = update_sensors()
    #print(left_color)
    
   

    # Handle state transitions
    
    transition_state(left_color, right_color)
    switch(state)
    #print(lane_state)
    #end=time.time()-start
    #print(end)

    


# Write your program here.
ev3.speaker.beep()
