#!/usr/bin/env python3

## This code test the basic movements to follow a light using LDR sensors.

import sys 
import time
from aurigapy import *
from datetime import datetime
import time
import random


def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

#Create robot and bluetooth path
robot_8 = AurigaPy(debug=False)
robot_8_bluetooth = "/dev/rfcomm8" #/dev/rfcomm8 COM7


#Try to connect with the robot
try:
    robot_8.connect(robot_8_bluetooth)
    print("Connected")    
except: # catch *all* exceptions
    print("Error: " + sys.exc_info()[0])

#Wait 2 seconds
time.sleep(2)

#threshold that take care the sensor error
epsilon = 100

try:

while True:
    #Read Sensors and show
    light1 = robot_8.get_light_sensor_onboard(1)
    print("Light1: %r > %r " % (timestamp(), light1))
    
    light2 = robot_8.get_light_sensor_onboard(2)
    print("Light2: %r > %r " % (timestamp(), light2))
    
    #threshold to stop the program
    if light1 < 50 and light2 < 50:
        break
    #Follow the light
    if light1 > (light2 + epsilon):
        robot_8.set_command(command="left", speed=70)
        time.sleep(0.2)
    
    elif light2 > (light1 + epsilon):
        robot_8.set_command(command="right", speed=70)
        time.sleep(0.2)
    else:
        robot_8.set_command(command="forward", speed=70)
        time.sleep(0.2)
        

robot_8.reset_robot()
print("Closing")
robot_8.close()    
