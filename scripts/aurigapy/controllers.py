#!/usr/bin/env python3


## Este script se encarga de recoger los controladores

from aurigapy import *
import time

#TODO: Añadir las funiones que vayan haciendo paco y abel
#Todo lo que hay hasta el momento son EJEMPLOS (cambiad lo que os parezca)


# Este struct contendrá las salidas que hay que aplicar a cada motor
class Actions:
    def __init__(self):
        print("Init Class Actions")
        
        self.movement_motors_pwm = 0
        self.command = "forward"
        self.tool_motor_pwm = 0


##------------------CONTROLADORES------------------##        

# Controlador específico para parar motores
def controllerStop(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Stop")
    
    robot.st_actions.movement_motors_pwm = 0
    robot.st_actions.command = "forward"

# Controlador específico que se utiliza para avanzar a la máxima velocidad permitida por configuración
def controllerMovingForwardMax(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Forward Max")

    robot.st_actions.movement_motors_pwm = robot.st_config.max_speed_pwm_value
    robot.st_actions.command = "forward"        
        
