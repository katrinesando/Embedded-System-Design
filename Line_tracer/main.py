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
from collections import *
#from collections import counter

# Create your objects here.
ev3 = EV3Brick()

# Initialize the motors and sensors.
motor_left = Motor(Port.C) #Check for correct Port 
motor_right = Motor(Port.B) 
sensor_left= ColorSensor(Port.S3)
sensor_right= ColorSensor(Port.S4)
# color_list_left = [] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED
# color_list_right = [] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED

color_list_left = [(94, 70, 20),(215, 30, 96),(133, 37, 72),(208, 78, 61),(63, 74, 70),(14, 79, 58)] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED
color_list_right = [(93, 75, 12),(192, 48, 70),(138,57,56),(201, 82, 41), (84, 79, 54),(17, 80, 30)] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED


STATES=["DRIVE","STOP","SLOW","TURN_LEFT","TURN_RIGHT","SWITCH_LANE","HOLD"]#All possible states the robot can have 
LANE_STATES=["UNKNOWN","LEFT_LANE","RIGHT_LANE"]
rounds=1
state=STATES[1]
lane_state=LANE_STATES[0]
Speed = 200
left_array=deque([0])
right_array=deque([0])
left = None
right = None

# Initialize the drive base.
robot = DriveBase(motor_left, motor_right, wheel_diameter=55, axle_track=145) #Check for correct Parameter 

# while True:
#     if ev3.buttons.pressed() == True:
#         print ("pressed")
#     h, s, v = rgb_to_hsv(sensor_left.rgb())
#     color_right = rgb_to_hsv(sensor_right.rgb())
#     # Print results
#     print('H: {0}\t S: {1}\t V: {2}'.format(h,s,v))
#     print(color_right)
#     wait(1000)

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

def proc(num, off):
    n = off*num
    return num-n, num+n

# calculates allowed range for hsv values
def procentRange(h,s,v, color_list):
    procH = proc(color_list[0],0.25)
    procS = proc(color_list[1],0.30)
    procV = proc(color_list[2],0.15)
    if (procH[0]<= h <= procH[1]) and (procS[0]<= s <=procS[1]) and (procV[0] <= v <= procV[1]):
        return True
    return False

# finds color in list with allowed offset
def find_color(): #Update sensor readings
    global right, left
    h_l,s_l,v_l = rgb_to_hsv(sensor_left.rgb())
    h_r,s_r,v_r = rgb_to_hsv(sensor_right.rgb())
    # print('H: {0}\t S: {1}\t V: {2}'.format(h_l, s_l, v_l))
    # print(rgb_to_hsv(sensor_right.rgb()))
    if (h_l == 0 and s_l == 0 and v_l == 0) and (h_r == 0 and s_r == 0 and v_r == 0):
        return None, None
    for i in color_list_left:
        if procentRange(h_l,s_l,v_l,i):
            left = i

    for i in color_list_right:
        if procentRange(h_r,s_r,v_r,i):
            right = i

    return left,right

def update_sensors(): #Update sensor readings
    global left_array
    global right_array

    color_left, color_right = find_color()
    left_array.append(color_num(color_left, color_list_left))
    right_array.append(color_num(color_right, color_list_right))

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
   
# function changes state depending of sensor outputs
def transition_state(color_left, color_right): 
    global state
    global lane_state
    global rounds

    if left_color == 1 and right_color == 1: # Black
        state=STATES[0] # Move forward

    if left_color == 1 and right_color == 2: # Black / White
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[1]
        state=STATES[3]

    if left_color == 2 and right_color == 1: # White / Black
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[2]
        state=STATES[4]
        
    if left_color == 3: # Green
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[1]
        state=STATES[4]

    if right_color == 3: # Green
        if lane_state==LANE_STATES[0]:
            lane_state=LANE_STATES[2]
        state=STATES[3]

    if left_color == 4 or right_color == 4: #Blue - 3 sec stop
        state=STATES[6]

    if left_color == 5 or right_color == 5: #Yellow - slow down 
        state=STATES[2]
   
    if left_color == 6 and right_color == 6: #Red - lane switch
        if rounds<1:
            state=STATES[1]
        else:
            state=STATES[5]

    if left_color==0 and right_color==0: # None
        state=STATES[1]
        lane_state=LANE_STATES[0]
        rounds=1


def color_num(color, color_list):
    if color == None:
        return 0
    elif color == color_list[0]: # black
        return 1
    elif color == color_list[1]: # white 
        return 2
    elif color == color_list[2]: # green
        return 3
    elif color ==color_list[3]:  # blue
        return 4
    elif color == color_list[4]: # yellow
        return 5
    elif color == color_list[5]: # red
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

    # Handle state transitions
    transition_state(left_color, right_color)
    left = None
    right = None
    switch(state)
    #print(lane_state)
    #end=time.time()-start
    #print(end)
