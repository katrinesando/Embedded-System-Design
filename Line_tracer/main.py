#!/usr/bin/env pybricks-micropython
import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color # type: ignore
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.iodevices import Ev3devSensor
from pybricks.media.ev3dev import SoundFile, ImageFile

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# Initialize the motors and sensors.
motor_left = Motor(Port.C) #Check for correct Port 
motor_right = Motor(Port.B) 
sensor_left= Ev3devSensor(Port.S3)
sensor_right= Ev3devSensor(Port.S4)
color_list_left = [] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED
color_list_right = [] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED


STATES=["DRIVE","STOP","SLOW","TURN_LEFT","TURN_RIGHT","SWITCH_LANE","HOLD"]#All possible states the robot can have 
LANE_STATES=["UNKNOWN","LEFT_LANE","RIGHT_LANE"]
rounds=1
state=STATES[1]
lane_state=LANE_STATES[0]
Speed = 100

# # Initialize the drive base.
robot = DriveBase(motor_left, motor_right, wheel_diameter=55, axle_track=145) #Check for correct Parameter 

def get_colors():
    while len(color_list_left) <= 6:
        with open('color.txt', 'w') as cf:
        # color_f = open('color.txt', 'w')
            pressed = ev3.buttons.pressed() 
            if pressed:
                color_left = sensor_left.read('RGB-RAW')
                color_right = sensor_right.read('RGB-RAW')
                r, g, b = sensor_left.read('RGB-RAW')
                # r, g, b = sensor_right.read('RGB-RAW')
                cf.write("hej")
                # cf.write("{0}{1}{2}\n".format(r, g, b))
                color_list_left.append(color_left)
                color_list_right.append(color_right)
                print('R: {0}\t G: {1}\t B: {2}'.format(r, g, b))
                wait(500)
    # while color_sensor.color() in POSSIBLE_COLORS:
    #         pass

def update_sensors(): #Update sensor readings
    r_l,g_l,b_l = sensor_left.read('RGB-RAW')
    r_r,g_r,b_r = sensor_right.read('RGB-RAW')
    left = None
    right = None
    # color_right = sensor_right.color()
    for i in color_list_left:
        print('R: {0}\t G: {1}\t B: {2}'.format(r_l, g_l, b_l))
        if inrange(r_l,g_l,b_l,i):
            left = i
        else:
            print ("no")
            left = None
        wait(200)
    for i in color_list_right:
        if inrange(r_r,g_r,b_r,i):
            right_color = i
        else:
            print ("no")
            right = None
        wait(200)
    return left,right

def inrange(r,g,b, color_list):
    offset = 3
    if (color_list[0]-offset <= r <= color_list[0]+offset) and (color_list[1]-offset <= g <= color_list[1]+offset )and (color_list[2]-offset <= b <= color_list[2]+offset):
        return True 
    return False


# #function changes state depending of sensor outputs
def transition_state(color_left, color_right): 
    global state
    global lane_state
    global rounds

    if left_color == color_list_left[0] and right_color == color_list_right[0]:#black
        state=STATES[0] # Move forward

    if left_color == color_list_left[2]:#green
        state=STATES[4]

    if right_color==color_list_right[2]: #green
        state=STATES[3]

    if left_color == color_list_left[0] and right_color == color_list_right[1]: #Black / white
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[1]
        state=STATES[3]

    if left_color == color_list_left[1] and right_color == color_list_right[0]: # white / black
        state=STATES[4]
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[2]
        
    if left_color == color_list_left[4]: # yellow
        state=STATES[2]
    if right_color == color_list_right[4]: # yellow
        state=STATES[2]

    if left_color == color_list_left[5] and right_color == color_list_right[5]: # red
        if rounds<=0:
            state=STATES[1]
        state=STATES[5]
        
    if left_color == color_list_left[3] and right_color == color_list_right[3]: # blue
        state=STATES[6]

    if left_color==None and right_color==None: # none
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
        wait(1000)
    elif state ==  "TURN_LEFT":
        robot.drive(Speed,-45)
    elif state ==  "TURN_RIGHT":
        robot.drive(Speed,45)
    elif state ==  "SWITCH_LANE":
        if lane_state=="LEFT_LANE":
            robot.drive(Speed,45)
            wait(600)# timing needs to be relativ to the speed. (maybe wait(30000/speed)). 30000 is the distance
            robot.drive(Speed,0)
            wait(1000)
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
        else:
            print("No lane detected")
            robot.drive(Speed,45)
    elif state == "HOLD":
        robot.drive(0,0)
        wait(3000)
        robot.drive(Speed,0)
        wait(1000)

#main loop of the programm
while True:
    # Update sensor readings
    get_colors()
    left_color, right_color = update_sensors()
    #print(left_color)
    
    # Handle state transitions
    wait(10)
    transition_state(left_color, right_color)
    switch(state)
    # print(state)

    


# Write your program here.
