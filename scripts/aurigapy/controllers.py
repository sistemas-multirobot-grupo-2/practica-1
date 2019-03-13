#!/usr/bin/env python3


## Este script se encarga de recoger los controladores

import description_constants as constants
from aurigapy import *
import time

#TODO: Añadir controlador a bajo nivel de seguimiento de linea
#TODO: Añadir variables para la pinza y mejorar la funcion sin usar delays

# Este struct contendrá las salidas que hay que aplicar a cada motor
class Actions:
    def __init__(self):
        print("Init Class Actions")
        
        self.movement_motors_pwm = 0.0
        self.command = constants.FORWARD
        self.tool_motor_pwm = 0
        
        self.object_picked = False
        self.grasping = False      


##------------------CONTROLADORES------------------##        

# Controlador específico para parar motores
def controllerStop(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Stop")
    
    elif(robot.mode == 'real_robot'): #Robot real
        robot.st_actions.movement_motors_pwm = 0.0
        robot.st_actions.command = constants.FORWARD
    
    else:
        robot.st_actions.movement_motors_pwm = 0.0
        robot.st_actions.command = constants.FORWARD

# Controlador específico que se utiliza para avanzar a la máxima velocidad permitida por configuración
def controllerMovingForwardMax(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Forward Max")
    
    elif(robot.mode == 'real_robot'): 
        robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm
        robot.st_actions.command = constants.FORWARD
    
    else:
        robot.st_actions.movement_motors_pwm = 0.0
        robot.st_actions.command = constants.FORWARD        

def controllerMovingForwardProportional(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Forward Proportional")
    
    elif(robot.mode == 'real_robot'):
        if(robot.rol == constants.LEADER):
            print("prop1")
            if(robot.st_meas.light_sensor_value <= robot.st_config.light_threshold_min):
                robot.st_actions.movement_motors_pwm = 0.0
                
            elif(robot.st_meas.light_sensor_value >= robot.st_config.light_threshold_max):
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm
                
            else:
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm - ((robot.st_config.max_movement_motors_pwm - robot.st_config.min_movement_motors_pwm) * (robot.st_meas.light_sensor_value - robot.st_config.light_threshold_min)) / float(robot.st_config.light_threshold_max - robot.st_config.light_threshold_min)                                 

        elif(robot.rol == constants.FOLLOWER):
            if(robot.st_meas.ultrasensor_distance < robot.st_config.near_object_threshold):
                robot.st_actions.movement_motors_pwm = 0.0
                
            elif(robot.st_meas.ultrasensor_distance > robot.st_config.far_object_threshold):
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm
                
            else:
                robot.st_actions.movement_motors_pwm = robot.st_config.min_movement_motors_pwm + ((robot.st_config.max_movement_motors_pwm- robot.st_config.min_movement_motors_pwm) * (robot.st_meas.ultrasensor_distance - robot.st_config.near_object_threshold)) / (robot.st_config.far_object_threshold - robot.st_config.near_object_threshold)                                 
       
        else:
            robot.st_actions.movement_motors_pwm = 0.0
    
    else:
        robot.st_actions.movement_motors_pwm = 0.0
    
    robot.st_actions.command = constants.FORWARD 
        
def controllerMovingBackwardMax(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Backward Max")
    
    elif(robot.mode == 'real_robot'):
        robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm
        robot.st_actions.command = constants.BACKWARD
    
    else:
        robot.st_actions.movement_motors_pwm = 0
        robot.st_actions.command = constants.BACKWARD       
        
def controllerMovingBackwardProportional(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Backward Proportional")
    
    elif(robot.mode == 'real_robot'):
        if(robot.rol == constants.LEADER):
            if(robot.st_meas.light_sensor_value < robot.st_config.light_threshold_min):
                robot.st_actions.movement_motors_pwm = 0
                
            elif(robot.st_meas.light_sensor_value > robot.st_config.light_threshold_max):
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm
                
            else:
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm - ((robot.st_config.max_movement_motors_pwm- robot.st_config.min_movement_motors_pwm) * (robot.st_meas.light_sensor_value - robot.st_config.light_threshold_min)) / (robot.st_config.light_threshold_max - robot.st_config.light_threshold_min)                                 
       
        elif(robot.rol == constants.FOLLOWER):
            if(robot.st_meas.ultrasensor_distance < robot.st_config.near_object_threshold):
                robot.st_actions.movement_motors_pwm = 0
                
            elif(robot.st_meas.ultrasensor_distance > robot.st_config.far_object_threshold):
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm
                
            else:
                robot.st_actions.movement_motors_pwm = robot.st_config.min_movement_motors_pwm + ((robot.st_config.max_movement_motors_pwm- robot.st_config.min_movement_motors_pwm) * (robot.st_meas.ultrasensor_distance - robot.st_config.near_object_threshold)) / (robot.st_config.far_object_threshold - robot.st_config.near_object_threshold)                                 
       
        else:
            robot.st_actions.movement_motors_pwm = 0
    
    else:
        robot.st_actions.movement_motors_pwm = 0
    
    robot.st_actions.command = constants.BACKWARD 
        
def controllerPickPlace(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Pick and Place")        
    
    elif(robot.mode == 'real_robot'):
        robot.mobile_robot.gripper("open", 7, 1)
        robot.tool_closed = False #CAMBIADO
        time.sleep(4)
        
        #Cerrar Pinza
        robot.mobile_robot.gripper("close", 7, 1)
        robot.tool_closed = True #CAMBIADO
        time.sleep(2)
        
    else:
        #Cerrar Pinza
        robot.mobile_robot.gripper("close", 7, 1)
        robot.tool_closed = True #CAMBIADO
        time.sleep(2)
        

        
