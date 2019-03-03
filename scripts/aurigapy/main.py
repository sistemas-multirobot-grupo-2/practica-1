#!/usr/bin/env python3

import sys
import threading
import argparse
from robot import Robot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default='simulation', help='simulation/real_robot')
    args = parser.parse_args()
    
    try:
        robot = Robot(args.mode,bluetooth_path="/dev/rfcomm8",robot_rol="leader",
                        robot_sensors_list=["ultrasonic","light","light"],
                        robot_sensor_ports_list=[9,10,11,])
        
        robot.run_main()
        # falta añadir multithreading
        
        
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')    
    except:
        if(args.mode == 'real_robot'):
            robot.mobile_robot.reset_robot()
            robot.mobile_robot.close()
            
        print("Error: " + str(sys.exc_info()[0]))
        pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
