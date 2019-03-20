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
        self.left_motor_pwm = 0.0
        self.right_motor_pwm = 0.0

        self.last_direction = constants.FORWARD

        self.command = constants.FORWARD
        self.tool_motor_pwm = 0
        
        self.object_picked = False
        self.grasping = False      



##------------------SIGUE LINEAS------------------##        
"""def customSpeeds(robot, speed_L, speed_R):
    # Need to concatenate the hex sequence ff 55 07 00 02 05 <speedleft> <speedright> to the bot's output
    # Since the line follower direction control requires of custom speeds for each wheel, it's convenient to directly call
    # the _write method with a customized string

    # Minor changes to the usual callback generation
    rp = Response.generate_response_block(Frame.FRAME_TYPE_ACK, timeout=2)
    robot.add_responder(rp)

    # Generate hex string based on speeds
    data = bytearray([0xff, 0x55, 0x07, 0x00, 0x02, 0x5] +
    short2bytes(speed_L) +
    short2bytes(speed_R))

    # Write the hex string directly to the bot
    robot._write(data)
    # Wait for callback
    rp.wait_blocking()
"""

def lineFollower(line_value, base_speed, base_turn, lastSpeedo):
    
    left_speed = 0.0
    right_speed = 0.0
    command = constants.FORWARD

    if(line_value == 0):
        if(lastSpeedo == constants.FORWARD):
            customSpeeds(ap,-base_speed,base_speed)
        elif(lastSpeedo == constants.BACKWARD):
            customSpeeds(ap,base_speed,-base_speed) # Halt: EotL
        elif(lastSpeedo == constants.LEFT):
            customSpeeds(ap,-base_speed,base_speed+5) # We "trick" the system into readjusting itself, preventing a possible overcompensation in the turn
        elif(lastSpeedo == constants.RIGHT):
            customSpeeds(ap,-base_speed+5,base_speed) # Same as before, but this time favouring a slight left turn instead of a right one
        lastSpeedo = constants.FORWARD

    elif(line_value == 1):
        if(lastSpeedo == constants.FORWARD):
            customSpeeds(ap,-base_turn,-base_turn)
        elif(lastSpeedo == constants.BACKWARD):
            customSpeeds(ap,base_speed,base_turn)
        elif(lastSpeedo == constants.LEFT):
            customSpeeds(ap,-base_speed,-base_turn) # Pronounced left turn, speed up slightly
        elif(lastSpeedo == constants.RIGHT):
            customSpeeds(ap,-base_speed,-base_turn) # Sharp "Z" turn, slow down slightly
        lastSpeedo = constants.LEFT

    elif(line_value == 2):
        if(lastSpeedo == constants.FORWARD):
            customSpeeds(ap,base_turn,base_speed)
        elif(lastSpeedo == constants.BACKWARD):
            customSpeeds(ap,-base_turn,-base_speed)
        elif(lastSpeedo == constants.LEFT):
            customSpeeds(ap,base_turn,base_speed) # Sharp "Z" turn, slow down slightly
        elif(lastSpeedo == constants.RIGHT):
            customSpeeds(ap,base_turn,base_speed) # Pronounced right turn, speed up slightly
        lastSpeedo = constants.RIGHT

    elif(line_value == 3):
        customSpeeds(ap,base_speed,-base_speed)
        lastSpeedo = constants.BACKWARD
    #   if(lastSpeedo == constants.FORWARD):
    #       customSpeeds(ap,base_speed,-base_speed) # Out of line after forwards action, go backwards
    #       lastSpeedo = constants.BACKWARD
    #   elif(lastSpeedo == constants.BACKWARD):
    #       customSpeeds(ap,-base_speed,base_speed) # OOL after backwards action, go back forwards
    #       lastSpeedo = constants.FORWARD
    #   elif(lastSpeedo == constants.LEFT):
    #       customSpeeds(ap,base_speed,base_speed) # OOL after left turn, turn right
    #       lastSpeedo = constants.RIGHT
    #   elif(lastSpeedo == constants.RIGHT):
    #       customSpeeds(ap,-base_speed,-base_speed) # OOL after right turn, turn left
    #       lastSpeedo = constants.LEFT
    return right_speed, left_speed, command, lastSpeedo

##------------------CONTROLADORES------------------##        
# Controlador específico para parar motores
def controllerStop(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Stop")
    
    elif(robot.mode == 'real_robot'): #Robot real
        robot.st_actions.left_motor_pwm = 0.0
        robot.st_actions.right_motor_pwm = 0.0
        robot.st_actions.command = constants.FORWARD
    
    else:
        robot.st_actions.left_motor_pwm = 0.0
        robot.st_actions.right_motor_pwm = 0.0
        robot.st_actions.command = constants.FORWARD

# Controlador específico que se utiliza para avanzar a la máxima velocidad permitida por configuración
def controllerMovingForwardMax(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Forward Max")
    
    elif(robot.mode == 'real_robot'): 
        #robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm
        robot.st_actions.command = constants.FORWARD
        robot.st_actions.right_motor_pwm, robot.st_actions.left_motor_pwm, robot.st_actions.command, robot.st_actions.last_direction = lineFollower(robot.st_meas.line_value, robot.st_config.base_speed, robot.st_config.base_turn, robot.st_actions.last_direction)
    
    else:
        robot.st_actions.left_motor_pwm = 0.0
        robot.st_actions.right_motor_pwm = 0.0
        robot.st_actions.command = constants.FORWARD        

def controllerMovingForwardProportional(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control - Forward Proportional")
    
    elif(robot.mode == 'real_robot'):
        if(robot.rol == constants.LEADER):
            if(robot.st_meas.light_sensor_value <= robot.st_config.light_threshold_min):
                robot.st_actions.left_motor_pwm = 0.0
                robot.st_actions.right_motor_pwm = 0.0
                
            elif(robot.st_meas.light_sensor_value >= robot.st_config.light_threshold_max):
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm
                
            else:
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm - ((robot.st_config.max_movement_motors_pwm - robot.st_config.min_movement_motors_pwm) * (robot.st_meas.light_sensor_value - robot.st_config.light_threshold_min)) / float(robot.st_config.light_threshold_max - robot.st_config.light_threshold_min)                                 

        elif(robot.rol == constants.FOLLOWER):
            if(robot.st_meas.ultrasensor_distance < robot.st_config.near_object_threshold):
                robot.st_actions.left_motor_pwm = 0.0
                robot.st_actions.right_motor_pwm = 0.0
                
            elif(robot.st_meas.ultrasensor_distance > robot.st_config.far_object_threshold):
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm
                
            else:
                robot.st_actions.movement_motors_pwm = robot.st_config.max_movement_motors_pwm - ((robot.st_config.max_movement_motors_pwm- robot.st_config.min_movement_motors_pwm) * (robot.st_meas.ultrasensor_distance - robot.st_config.near_object_threshold)) / (robot.st_config.far_object_threshold - robot.st_config.near_object_threshold)                                 
       
        else:
            robot.st_actions.left_motor_pwm = 0.0
            robot.st_actions.right_motor_pwm = 0.0
    
    else:
        robot.st_actions.left_motor_pwm = 0.0
        robot.st_actions.right_motor_pwm = 0.0
    
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
        


        
