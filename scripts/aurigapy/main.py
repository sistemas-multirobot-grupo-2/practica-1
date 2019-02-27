#!/usr/bin/env python3

import sys
import threading
from robot import Robot


def main():
    try:
        #robot_1 = Robot(bluetooth_path="/dev/rfcomm1")
        robot_8 = Robot(bluetooth_path="/dev/rfcomm8")
        
        robot_8.run_main()
        # falta añadir multithreading
        
        
        
    except:
        #robot_1.close()
        robot_8.close()
        print("Error: " + str(sys.exc_info()[0]))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    except: # catch *all* exceptions
        print("Error: " + sys.exc_info()[0])
