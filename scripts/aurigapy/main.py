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
        robot1 = Robot(name="Robot1",mode=args.mode,bluetooth_path="/dev/rfcomm8",robot_rol="leader",
                        robot_sensors_list=["light","light","line"],
                        robot_sensor_ports_list=[9,10,11])
        
        robot2 = Robot(name="Robot2",mode=args.mode,bluetooth_path="/dev/rfcomm1",robot_rol="follower",
                        robot_sensors_list=["ultrasonic","light","light","line"],
                        robot_sensor_ports_list=[9,10,11,12])
        
        
        t1 = threading.Thread(target=robot1.run_main)
        t2 = threading.Thread(target=robot2.run_main)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')    
    except:
        if(args.mode == 'real_robot'):
            robot1.mobile_robot.reset_robot()
            robot1.mobile_robot.close()
            
        print("Error: " + str(sys.exc_info()[0]))
        pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
