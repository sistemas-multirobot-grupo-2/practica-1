#!/usr/bin/env python3


##-------Robots-------##

# Estados
STOP                              =  0
MOVING_FORWARD_MAX                =  1
MOVING_FORWARD_PROPORTIONAL       =  2
MOVING_BACKWARD_MAX               =  3
MOVING_BACKWARD_PROPORTIONAL      =  4
PICK_PLACE_OBJECT                 =  5
UNDEFINED                         = -1
EMERGENCY                         = -2

# Roles
LEADER      =  0
FOLLOWER    =  1
UNDEFINED   = -1

# Codigos de Error
EXECUTION_ERROR         = -1
EXECUTION_SUCCESSFUL    =  0


##-------Sensores-------##

#Distancia - ultrasonidos
IMPOSSIBLE_DISTANCE     = -1
MIN_ULTRASONIC_VALUE    =  0 #Minimum detectable value for the distance sensor
MAX_ULTRASONIC_VALUE    =  400 #Maximum detectable value for the distance sensor
ULTRASONIC_ERROR        =  5

UNKNOWN_OBJECT_DETECTED     = -1
COLLISION_OBJECT_DETECTED   =  0
NEAR_OBJECT_DETECTED        =  1
FAR_OBJECT_DETECTED         =  2

#Luz
IMPOSSIBLE_LIGHT_VALUE  = -1
MIN_LIGHT_VALUE         =  1 #Minimum detectable value for the light sensor
MAX_LIGHT_VALUE         =  1023 #Maximum detectable value for the light sensor

NO_LIGHT_DETECTED       =  0
LOW_LIGHT_DETECTED      =  1
HIGH_LIGHT_DETECTED     =  2
UNKNOWN_LIGHT_DETECTED  = -1

#Linea
BOTH_LINES_DETECTED     =  0
LEFT_LINE_DETECTED      =  1
RIGHT_LINE_DETECTED     =  2
ANY_LINE_DETECTED       =  3
UNKNOWN_LINE_VALUE      = -1


##-------Controladores-------##
FORWARD     = "forward"
BACKWARD    = "backward"
RIGHT       = "right"
LEFT        = "left"

# Velocidades siguelíneas
BASE_SPEED = 40
BASE_TURN = 25




