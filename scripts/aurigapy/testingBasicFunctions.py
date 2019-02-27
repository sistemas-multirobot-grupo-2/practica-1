#!/usr/bin/env python3

## This code test the basic sensors, leds, sounds and movements

import sys 
import time
from aurigapy import *
from datetime import datetime
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

#test: sound and leds
robot_8.set_led_onboard(0,r=0,g=0,b=0)
for i in range(11):
    robot_8.play_sound(sound=i * 2 + 131, duration_ms=100)
    time.sleep(0.2)
    
    robot_8.set_led_onboard(i+1,r=255,g=0,b=0)
    
time.sleep(2)


#test: sensors
#estate: GREEN
robot_8.set_led_onboard(0,r=0,g=255,b=0)    
for i in range(20):
    #Read Sensors and show     
    dist = robot_8.get_ultrasonic_reading(10)
    print("Ultrasonic: %r > %r " % (timestamp(), dist))
    
    temp = robot_8.get_temperature_sensor_onboard()
    print("Temperature: %r > %r " % (timestamp(), temp))
    
    compass = robot_8.get_compass_sensor(7)
    print("Compass: %r > %r \n" % (timestamp(), compass))
    
    x = robot_8.get_gyro_sensor_onboard("x")
    y = robot_8.get_gyro_sensor_onboard("y")
    z = robot_8.get_gyro_sensor_onboard("z")
    
    giro = str((x, y, z))
    print("Giro: %r > %r " % (timestamp(), giro))
    
    light1 = robot_8.get_light_sensor_onboard(1)
    print("Light1: %r > %r " % (timestamp(), light1))
    
    light2 = robot_8.get_light_sensor_onboard(2)
    print("Light2: %r > %r " % (timestamp(), light2))
    
    time.sleep(1)

time.sleep(2)

    
#test: move forward incrementally
#estate: BLUE
robot_8.set_led_onboard(0,r=0,g=0,b=255)
for i in range(10):
    robot_8.move_to(command="forward", degrees=500+i*50, speed=i*5 + 50)

time.sleep(2)    
 
#test: combine movements and ultrasonic sensor
#estate: YELLOW  
robot_8.set_led_onboard(0,r=255,g=255,b=0)
dist = 400 #max distance
#move forward while no object is detected
while dist > 100:
    dist = robot_8.get_ultrasonic_reading(10)
    robot_8.move_to(command="forward", degrees=200, speed=100)

#move backward and left when an object is detected    
time.sleep(1)
robot_8.move_to(command="backward", degrees=300, speed=70)
time.sleep(1)
robot_8.move_to(command="left", degrees=300, speed=70)


#End tests
time.sleep(2)
robot_8.set_led_onboard(0,r=0,g=0,b=0)

robot_8.reset_robot()
print("Closing")
robot_8.close()


