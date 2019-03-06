#!/usr/bin/env python3


## Este script se encarga de recoger los controladores

from aurigapy import *
import time

#TODO: Añadir controlador a bajo nivel de seguimiento de linea
#TODO: Añadir variables para la pinza y mejorar la funcion sin usar delays

FORWARD     = "forward"
BACKWARD    = "backward"

# Este struct contendrá las salidas que hay que aplicar a cada motor
class Actions:
    def __init__(self):
        print("Init Class Actions")
        
        self.movement_motors_pwm = 0
        self.command = FORWARD
        self.tool_motor_pwm = 0
        
        self.object_picked = False
        self.finished_grasping = False      


##------------------CONTROLADORES------------------##        

# Controlador específico para parar motores
def controllerStop(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Stop")
    
    elif(robot.mode == 'real_robot'): #Robot real
        robot.st_actions.movement_motors_pwm = 0
        robot.st_actions.command = FORWARD
    
    else:
        robot.st_actions.movement_motors_pwm = 0
        robot.st_actions.command = FORWARD

# Controlador específico que se utiliza para avanzar a la máxima velocidad permitida por configuración
def controllerMovingForwardMax(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Forward Max")
    
    elif(robot.mode == 'real_robot'): 
        robot.st_actions.movement_motors_pwm = robot.st_config.max_speed_pwm_value
        robot.st_actions.command = FORWARD
    
    else:
        robot.st_actions.movement_motors_pwm = 0
        robot.st_actions.command = FORWARD        

def controllerMovingForwardProportional(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Forward Proportional")

    elif(robot.mode == 'real_robot'):
        robot.st_actions.movement_motors_pwm = robot.st_config.min_movement_motors_pwm + ((robot.st_config.max_movement_motors_pwm- robot.st_config.min_movement_motors_pwm) * (robot.st_data.light_sensor_value - robot.st_config.light_threshold_min)) / (robot.st_config.light_threshold_max - robot.st_config.light_threshold_min)                                 
        robot.st_actions.command = FORWARD
    
    else:
        robot.st_actions.movement_motors_pwm = 0
        robot.st_actions.command = FORWARD 
        
def controllerMovingBackwardMax(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Backward Max")
    
    elif(robot.mode == 'real_robot'):
        robot.st_actions.movement_motors_pwm = robot.st_config.max_speed_pwm_value
        robot.st_actions.command = BACKWARD
    
    else:
        robot.st_actions.movement_motors_pwm = 0
        robot.st_actions.command = BACKWARD       
        
def controllerMovingBackwardProportional(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Backward Proportional")
    
    elif(robot.mode == 'real_robot'):
        robot.st_actions.movement_motors_pwm = robot.st_config.min_movement_motors_pwm + ((robot.st_config.max_movement_motors_pwm- robot.st_config.min_movement_motors_pwm) * (robot.st_data.light_sensor_value - robot.st_config.light_threshold_min)) / (robot.st_config.light_threshold_max - robot.st_config.light_threshold_min)                                 
        robot.st_actions.command = BACKWARD
    
    else:
        robot.st_actions.movement_motors_pwm = 0
        robot.st_actions.command = BACKWARD 
        
def controllerPickPlace(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Pick and Place")        
    
    elif(robot.mode == 'real_robot'):
        robot.st_actions.finished_grasping = False
        
        # Abrir Pinza
        time.sleep(4)
        
        #Cerrar Pinza
        time.sleep(2)
        
        robot.st_actions.finished_grasping = True 
        
    else:
        robot.st_actions.finished_grasping = False
        #Cerrar Pinza
        
        

        
