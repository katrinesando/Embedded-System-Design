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
sensor_left= ColorSensor(Port.S3)
sensor_right= ColorSensor(Port.S4)
# color_list_left = [] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED
# color_list_right = [] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED

#For papers
# color_list_left = [(9,9,3),(59,56,76),(18,21,16),(5,10,16),(25,20,1),(31,10,6)] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED
# color_list_right = [(),(43,80,79),(18,43,23),(6,23,29),(28,42,5),(20,10,5)] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED


color_list_left = [(60,85,7),(243,21,89),(82,44,18),(180,57,7),(),()] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED
color_list_right = [(100,66,9),(171,44,77),(120,60,35),(168,76,21),(),()] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED

# For drift lane rgb
# color_list_left = [(12,13,1),((47,42,68)),((37,47,33)),((10,17,37)),((60,56,15)),((50,12,4))] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED
# color_list_right = [((8,13,1)),((41,73,73)),((25,58,32)),((8,28,39)),((36,54,10)),((31,13,5))] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED


# color_list_left = [(48,100,5),(240,40,5),(115,25,46),(48,77,58),(223,75,44),(11,87,55)] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED
# color_list_right = [(90,83,12),(235,79,17),(132,56,50),(85,81,53),(201,82,40),(22,87,50)] # 0=BLACK, 1=WHITE, 2=GREEN, 3=BLUE, 4=YELLOW, 5=RED


STATES=["DRIVE","STOP","SLOW","TURN_LEFT","TURN_RIGHT","SWITCH_LANE","HOLD"]#All possible states the robot can have 
LANE_STATES=["UNKNOWN","LEFT_LANE","RIGHT_LANE"]
rounds=1
state=STATES[1]
lane_state=LANE_STATES[0]
Speed = 100
left = None
right = None

# # Initialize the drive base.
robot = DriveBase(motor_left, motor_right, wheel_diameter=55, axle_track=145) #Check for correct Parameter 


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
    if ev3.buttons.pressed() == True:
        print ("pressed")
    r, g, b = rgb_to_hsv(sensor_left.rgb())
    color_right = rgb_to_hsv(sensor_right.rgb())
    # Print results
    print('R: {0}\t G: {1}\t B: {2}'.format(r, g, b))
    print(color_right)
    wait(1000)

def get_colors():
    while len(color_list_left) <= 5:
        with open('color.txt', 'w') as cf:
        # color_f = open('color.txt', 'w')
            pressed = ev3.buttons.pressed() 
            if pressed:
                color_left = rgb_to_hsv(sensor_left.rgb())
                print(color_left)
                color_right = rgb_to_hsv(sensor_right.rgb())
                r, g, b = sensor_left.rgb()
                cf.write("hej")
                color_list_left.append(color_left)
                color_list_right.append(color_right)
                print('R: {0}\t G: {1}\t B: {2}'.format(r, g, b))
                wait(500)

def update_sensors(): #Update sensor readings
    global right, left
    r_l,g_l,b_l = rgb_to_hsv(sensor_left.rgb())
    r_r,g_r,b_r = rgb_to_hsv(sensor_right.rgb())
    print('H: {0}\t S: {1}\t V: {2}'.format(r_l, g_l, b_l))
    print(rgb_to_hsv(sensor_right.rgb()))
    # color_right = sensor_right.color()
    if (r_l == 0 and g_l == 0 and b_l == 0) and (r_r == 0 and g_r == 0 and b_r == 0):
        return None, None
    for i in color_list_left:
        if procentRange(r_l,g_l,b_l,i):
            left = i

    for i in color_list_right:
        if procentRange(r_r,g_r,b_r,i):
            right = i

    return left,right

def inRange(r,g,b, color_list):
    OFFSET = 5
    if ((max(color_list[0]-OFFSET,0) <= r <= color_list[0]+OFFSET) and (max(color_list[1]-OFFSET,0) <= g <= color_list[1]+OFFSET )and (max(color_list[2]-OFFSET,0) <= b <= color_list[2]+OFFSET)):
        return True 
    return False

def proc(num, off):
    n = off*num
    return num-n, num+n

def procentRange(r,g,b, color_list):
    procR = proc(r,0.15)
    procG = proc(g,0.40)
    procB = proc(b,0.10)
    if (procR[0]<= r <= procR[1]) and (procG[0]<= g <=procG[1]) and (procB[0] <= b <= procB[1]):
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
        # print("none")
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
    get_colors()
    # Update sensor readings
    left_color, right_color = update_sensors()
    
    # Handle state transitions
    wait(10)
    transition_state(left_color, right_color)
    left = None
    right = None
    switch(state)
    print(state)

    


# Write your program here.