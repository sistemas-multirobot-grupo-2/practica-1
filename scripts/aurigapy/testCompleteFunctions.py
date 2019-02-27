#!/usr/bin/env python3

## This code test the basic sensors, leds, sounds and movements

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

#test: Compass & Ultrasonidos
#estate: GREEN
robot_8.set_command(command="forward", speed=70)
temp = robot_8.get_temperature_sensor_onboard()
print("Temperature: %r > %r " % (timestamp(), temp))
temp = robot_8.get_temperature_sensor_onboard()
print("Temperature: %r > %r " % (timestamp(), temp))
#time.sleep(5)

robot_8.set_command(command="forward", speed=0)

robot_8.reset_robot()
print("Closing")
robot_8.close()  

