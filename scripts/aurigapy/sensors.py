#!/usr/bin/env python3


## Este script se encarga de recoger las funciones que engloban la lectura y procesado de los datos


from aurigapy import *
import time

#TODO: Añadir las funiones que vayan haciendo yoinel y josemi
#Todo lo que hay hasta el momento son EJEMPLOS (cambiad lo que os parezca)


##-----Constantes y variables globales-----##

#Distancia - ultrasonidos
IMPOSSIBLE_DISTANCE     = -1
MIN_ULTRASONIC_VALUE    =  0 #Minimum detectable value for the distance sensor
MAX_ULTRASONIC_VALUE    =  400 #Maximum detectable value for the distance sensor

UNKNOWN_OBJECT_DETECTED = -1
NO_OBJECT_DETECTED      =  0
NEAR_OBJECT_DETECTED    =  1
FAR_OBJECT_DETECTED     =  2

#Luz
IMPOSSIBLE_LIGHT_VALUE  = -1
MIN_LIGHT_VALUE         =  1 #Minimum detectable value for the light sensor
MIN_LIGHT_VALUE         =  1023 #Maximum detectable value for the light sensor

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

# Este struct contendrá la información raw de los sensores
class Data:
    def __init__(self):
        print("Init Class Data")
        self.ultrasensor_distance = IMPOSSIBLE_DISTANCE #Distancia en cm leida por el sensor de distancia. "-1" para UNKNOWN
        self.light_sensor_value = IMPOSSIBLE_LIGHT_VALUE #Valor entre 0 y 1024 de intensidad de luz. "-1" para UNKNOWN
        self.line_detection = UNKNOWN_LINE_VALUE #0-los 2 on; 1-izq on; 2-der on; 3-ninguno. "-1" para UNKNOWN
        
# Este struct contendrá la información procesada de los sensores
class Information:
    def __init__(self):
        print("Init Class Information")
        self.ultrasensor_detection = NO_OBJECT_DETECTED #Posicion de un posible objeto (NEAR, FAR, NO)
        self.light_detection = UNKNOWN_LIGHT_DETECTED #Posicion de un posible objeto (HIGH, LOW, UNKNOWN)
        
        
##------------------Lectura------------------##        

# Función específica para leer el sensor de ultrasonidos.    
def readUltraSensor(robot, port):
    """
    Funcion para leer el sensor de distancia (ultrasonidos)

    :param self: Referencia a la instancia desde la que se llama a la funcion
    :param port: Puerto donde esta conectado el sensor de distancia

    :return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
    """
    error = False #Variable que contiene el valor de retorno

    #Actuar segun el modo en el que este el robot
    if robot.mode == 'simulation': #Simulacion
        print(robot.name + ": Leemos sensor ultrasonidos en el puerto " + str(port))
    elif robot.mode == 'real_robot': #Robot real
        #Comprobar que se ha cumplido el tiempo mínimo para consultar el sensor
        if(robot.current_time_ultrasonic - robot.previous_time_ultrasonic > robot.st_config.ultrasonic_sensor_reading_period_in_millis):
            robot.st_meas.ultrasensor_distance = robot.mobile_robot.get_ultrasonic_reading(port) #Actualizar medida anterior
            robot.previous_time_ultrasonic = time.time()*1000 #Actualizar tiempo de "ultima medida"
            
            if(robot.st_meas.ultrasensor_distance < MIN_ULTRASONIC_VALUE or robot.st_meas.ultrasensor_distance > MAX_ULTRASONIC_VALUE):
                robot.st_meas.ultrasensor_distance = IMPOSSIBLE_DISTANCE
            
        else:
            robot.st_meas.ultrasensor_distance = IMPOSSIBLE_DISTANCE
            error = True #Indicar error porque NO se ha podido leer la distancia (ha pasado demasiado poco tiempo)
    else: #Cualquier otro caso -> ERROR
        robot.st_meas.ultrasensor_distance = IMPOSSIBLE_DISTANCE
        error = True
        
    return error #Devolver la variable que indica si ha habido algun fallo
      
  

# Función específica para leer el sensor de luz
def readLightSensor(robot,port):
    """
    Funcion para leer el sensor de luz

    :param self: Referencia a la instancia desde la que se llama a la funcion
    :param port: Puerto donde esta conectado el sensor de luz

    :return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
    """
    error = False #Variable que contiene el valor de retorno
    
    #Actuar segun el modo en el que este el robot
    if(robot.mode == 'simulation'): #Simulacion
        print(robot.name + ": Procesamos la información del sensor de luz en el puerto " + str(port))
    
    elif(robot.mode == 'real_robot'): #Robot real
        robot.st_meas.light_sensor_value = robot.get_light_sensor_onboard(port) #Leer datos del sensor
        
        # sensor si la lectura da un valor ilogico
        if(robot.st_meas.light_sensor_value < MIN_LIGHT_VALUE or robot.st_meas.read_ligth > MAX_LIGHT_VALUE):
            robot.st_meas.light_sensor_value = IMPOSSIBLE_LIGHT_VALUE
            error = True
            
    else: #Cualquier otro caso -> ERROR
        robot.st_meas.light_sensor_value = IMPOSSIBLE_LIGHT_VALUE
        error = True
        
    return error #Devolver la variable que indica si ha habido algun fallo


# Función específica para leer el sensor de linea
def readLineSensor(robot,port):
    """
    Funcion para leer el sensor de linea

    :param robot: Referencia a la instancia desde la que se llama a la funcion
    :param port: Puerto donde esta conectado el sensor de linea

    :return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
    """
    error = False #Variable que contiene el valor de retorno
    
    #Actuar segun el modo en el que este el robot
    if robot.mode == 'simulation': #Simulacion
        print(robot.name + ": Procesamos la información del sensor de linea en el puerto " + str(port))
    
    elif robot.mode == 'real_robot': #Robot real
        robot.st_meas.line_detection = robot.get_line_sensor(port) #Leer informacion -> 0-los 2 on; 1-izq on; 2-der on; 3-ninguno    
        
        #Si se recibe un valor no-valido
        if robot.st_meas.line_detection<0 or robot.st_information.line_detection>3:
            robot.st_meas.line_detection = UNKNOWN_LINE_VALUE
            error = True #Indicar fallo
            
    else: #Cualquier otro caso -> ERROR
        robot.st_meas.line_detection = UNKNOWN_LINE_VALUE
        error = True
        
    return error #Devolver la variable que indica si ha habido algun fallo
                

##------------------Procesado------------------##  
      
# Procesador específico para extaer información acerca de la presencia de obstáculos en base a los datos del 
# sensor de ultrasonidos.
def processUltrasonicSensorData(robot,port):
    """
    Funcion para extaer informacion acerca de la presencia de obstaculos en base a los datos del sensor de distancia (ultrasonidos)

    :param self: Referencia a la instancia desde la que se llama a la funcion
    :param port: Puerto donde esta conectado el sensor de distancia (ultrasonidos)

    :return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
    """
    error = False #Variable que contiene el valor de retorno
    
    if(robot.mode == 'simulation'):
        print(robot.name + ": Procesamos la información del sensor de ultrasonidos en el puerto " + str(port))
    
    elif(robot.mode == 'real_robot'):
        if(robot.st_meas.ultrasensor_distance == IMPOSSIBLE_DISTANCE):
           robot.st_information.ultrasensor_detection = UNKNOWN_OBJECT_DETECTED
           error = True
  
        elif(robot.st_meas.ultrasensor_distance < robot.st_config.near_object_threshold):
            robot.st_information.ultrasensor_detection = NO_OBJECT_DETECTED 
        
        elif(robot.st_meas.ultrasensor_distance > robot.st_config.near_object_threshold and robot.st_meas.ultrasensor_distance < robot.st_config.far_object_threshold):
            robot.st_information.ultrasensor_detection = NEAR_OBJECT_DETECTED 
        
        elif(robot.st_meas.ultrasensor_distance > robot.st_config.far_object_threshold):
            robot.st_information.ultrasensor_detection = FAR_OBJECT_DETECTED
        else:
            robot.st_information.ultrasensor_detection = UNKNOWN_OBJECT_DETECTED 
    
    else: #Cualquier otro caso -> ERROR
        error = True
        robot.st_meas.ultrasensor_detection = UNKNOWN_OBJECT_DETECTED
        
    return error
        
    
# Procesador específico para extaer información acerca de la presencia de una fuente lumínica en base a los datos del 
# sensor de luz.
def processLightSensorData(robot,port):
    """
    Funcion para extaer informacion acerca de la presencia de obstaculos en base a los datos del sensor de luz

    :param self: Referencia a la instancia desde la que se llama a la funcion
    :param port: Puerto donde esta conectado el sensor de luz

    :return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
    """
    error = False #Variable que contiene el valor de retorno
    
    #Actuar segun el modo en el que este el robot
    if(robot.mode == 'simulation'): #Simulacion
        print(robot.name + ": Procesamos la información del sensor de luz en el puerto " + str(port))
        
    elif(robot.mode == 'real_robot'): #Robot real
        
        if(robot.st_meas.light_sensor_value == IMPOSSIBLE_LIGHT_VALUE):
            robot.st_information.light_detection = UNKNOWN_LIGHT_DETECTED #UNKNOWN_LIGHT_DETECTED=0
            error = True
        
        elif(robot.st_meas.read_ligth > robot.st_config.light_threshold_max):
            robot.st_information.light_detection = HIGH_LIGHT_DETECTED #HIGH_LIGHT_DETECTED=1
        
        elif(robot.st_meas.read_ligth > robot.st_config.light_threshold_min and robot.st_meas.read_ligth < robot.st_config.light_threshold_max):
            robot.st_information.light_detection = LOW_LIGHT_DETECTED #LOW_LIGHT_DETECTED=2
        
        elif(robot.st_meas.read_ligth < robot.st_config.light_threshold_min):
            robot.st_information.light_detection = NO_LIGHT_DETECTED 
        
        else: #Cualquier otro caso -> ERROR
            robot.st_information.light_detection = UNKNOWN_LIGHT_DETECTED
            error = True
            
    else: #Cualquier otro caso -> ERROR
        robot.st_information.light_detection = UNKNOWN_LIGHT_DETECTED
        error = True
        
    return error

        
# Procesador específico para extaer información acerca de la presencia de una linea.
def processLineSensorData(robot,port):
    """
    Funcion para extaer informacion acerca de la presencia de obstaculos en base a los datos del sensor de linea

    :param robot: Referencia a la instancia desde la que se llama a la funcion
    :param port: Puerto donde esta conectado el sensor de linea

    :return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
    """
    if robot.mode == 'simulation':
        print(robot.name + ": Procesamos la información del sensor de linea en el puerto " + str(port))
