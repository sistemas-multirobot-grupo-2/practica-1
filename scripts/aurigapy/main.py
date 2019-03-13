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
        
        robot1 = Robot(name="Robot1",mode=args.mode,bluetooth_path="/dev/rfcomm1",robot_rol="leader",
                        robot_sensors_list=["light","line"],
                        robot_sensor_ports_list=[1,9])
        
        robot2 = Robot(name="Robot2",mode=args.mode,bluetooth_path="/dev/rfcomm8",robot_rol="follower",
                        robot_sensors_list=["ultrasonic","line"],
                        robot_sensor_ports_list=[8,9])
        
        
        robot1.addSensors()
        robot2.addSensors()
        
        if(args.mode == "real_robot"):
            t1 = threading.Thread(target=robot1.run_main)
            t2 = threading.Thread(target=robot2.run_main)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        elif(args.mode == "simulation"):
            while True:
                robot1.run_main()
                robot2.run_main() 
              
        
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')  
        
        if(args.mode == 'real_robot'):
            robot1.mobile_robot.reset_robot()
            robot2.mobile_robot.reset_robot()
            robot1.mobile_robot.close()
            robot2.mobile_robot.close()
             
    except:
        print("Error: " + str(sys.exc_info()[0]))
        pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
