#!/usr/bin/env python3

import time
from aurigapy import *

"""
def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


robot_1 = AurigaPy(debug=False)
robot_1_bluetooth = "/dev/rfcomm1" #/dev/rfcomm8 COM7

try:
    robot_1.connect(robot_1_bluetooth)
    print("Connected")
    pass
except:
    print("Error")

time.sleep(2)

for i in range(12):
    robot_1.play_sound(sound=i * 2 + 131, duration_ms=100)
    time.sleep(0.5)
    
    r = robot_1.get_ultrasonic_reading(10)
    print("Ultrasonic: %r > %r " % (timestamp(), r))
    
    r = robot_1.get_temperature_sensor_onboard()
    print("Temperature: %r > %r " % (timestamp(), r))
    
    r = robot_1.get_compass_sensor(7)
    print("Compass: %r > %r \n" % (timestamp(), r))
    
    #robot_1.move_to(command="forward", degrees=100+i*20, speed=i*5 + 50)
    
    robot_1.set_led_onboard(i+1,r=255,g=0,b=0)
   

robot_1.reset_robot()
print("Closing")
robot_1.close()
"""

