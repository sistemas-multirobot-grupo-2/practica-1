#!/usr/bin/env python3


## Este script se encarga de recoger las funciones que engloban la lectura y procesado de los datos


from aurigapy import *
import time

#TODO: Añadir las funiones que vayan haciendo yoinel y josemi
#Todo lo que hay hasta el momento son EJEMPLOS (cambiad lo que os parezca)


##-----Constantes y variables globales-----##

#Distancia -ultrasonidos
IMPOSSIBLE_DISTANCE = -1.0
MIN_ULTRA_VALUE = 0 #Minimum detectable value for the distance sensor
MAX_ULTRA_VALUE = 400 #Maximum detectable value for the distance sensor
NEAR_OBJECT_THRESHOLD = 10 #An object closer than this will be considered a "near object"
FAR_OBJECT_THRESHOLD = 250 #An object closer than this will be considered a "far object"
NO_OBJECT_DETECTED = 0
NEAR_OBJECT_DETECTED = 1
FAR_OBJECT_DETECTED = 2

#Luz
MIN_LIGHT_VALUE = 1 #Minimum detectable value for the light sensor
MIN_LIGHT_VALUE = 1023 #Maximum detectable value for the light sensor
LIGHT_THRESHOLD = 700 #Threshold over what is considered a light indicator is present
UNKNOWN_LIGHT_DETECTED = 0
HIGH_LIGHT_DETECTED = 1
LOW_LIGHT_DETECTED = 2

# Este struct contendrá la información raw de los sensores
class Data:
    def __init__(self):
        print("Init Class Data")
        self.ultrasensor_distance = -1 #Distancia en cm leida por el sensor de distancia. "-1" para UNKNOWN
        self.read_light = -1 #Valor entre 0 y 1024 de intensidad de luz. "-1" para UNKNOWN

# Este struct contendrá la información procesada de los sensores
class Information:
    def __init__(self):
        print("Init Class Information")
        self.ultrasensor_detection = "NO_OBJECT_DETECTED" #Posicion de un posible objeto (NEAR, FAR, NO)
        self.line_detection = -1 #0-los 2 on; 1-izq on; 2-der on; 3-ninguno. "-1" para UNKNOWN
        self.light_detection = "UNKNOWN" #Posicion de un posible objeto (HIGH, LOW, UNKNOWN)
        
        
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
        if robot.current_time_ultrasonic - robot.previous_time_ultrasonic > robot.st_config.ultrasonic_sensor_reading_period_in_millis:
            robot.st_data.ultrasensor_distance = robot.mobile_robot.get_ultrasonic_reading(port) #Actualizar medida anterior
            robot.previous_time_ultrasonic = time.time()*1000 #Actualizar tiempo de "ultima medida"
        else:
            error = True #Indicar error porque NO se ha podido leer la distancia (ha pasado demasiado poco tiempo)
    else: #Cualquier otro caso -> ERROR
        robot.st_data.ultrasensor_distance = IMPOSSIBLE_DISTANCE
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
    if robot.mode == 'simulation': #Simulacion
        print(robot.name + ": Procesamos la información del sensor de luz en el puerto " + str(port))
    elif robot.mode == 'real_robot': #Robot real
        robot.st_data.read_ligth = robot.get_light_sensor_onboard(port) #Leer datos del sensor

        #Comprobar si la lectura da un valor logico
        if robot.st_data.read_ligth<MIN_LIGHT_VALUE or robot.st_data.read_ligth>MAX_LIGHT_VALUE:
            error = True
    else: #Cualquier otro caso -> ERROR
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
        robot.st_information.line_detection = robot.get_line_sensor(port) #Leer informacion -> 0-los 2 on; 1-izq on; 2-der on; 3-ninguno
        
        #Si se recibe un valor no-valido
        if robot.st_information.line_detection<0 or robot.st_information.line_detection>3:
            error = True #Indicar fallo
    else: #Cualquier otro caso -> ERROR
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
    
    #Actuar segun el modo en el que este el robot
    if robot.mode == 'simulation': #Simulacion
        print(robot.name + ": Procesamos la información del sensor de ultrasonidos en el puerto " + str(port))
    elif robot.mode == 'real_robot': #Robot real
        if robot.st_data.ultrasensor_distance < MIN_ULTRA_VALUE or robot.st_data.ultrasensor_distance > MAX_ULTRA_VALUE:
            error = True
        elif robot.st_data.ultrasensor_distance < NEAR_OBJECT_THRESHOLD:
            robot.st_information.ultrasensor_detection = NEAR_OBJECT_DETECTED #NEAR_OBJECT_DETECTED=1
        elif robot.st_data.ultrasensor_distance < FAR_OBJECT_THRESHOLD:
            robot.st_information.ultrasensor_detection = FAR_OBJECT_DETECTED #FAR_OBJECT_DETECTED=2
        else:
            robot.st_information.ultrasensor_detection = NO_OBJECT_DETECTED #NO_OBJECT_DETECTED=0
    else: #Cualquier otro caso -> ERROR
        error = True
        
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
    if robot.mode == 'simulation': #Simulacion
        print(robot.name + ": Procesamos la información del sensor de luz en el puerto " + str(port))
    elif robot.mode == 'real_robot': #Robot real
        if robot.st_data.read_ligth < MIN_LIGHT_VALUE or robot.st_data.read_ligth > MAX_LIGHT_VALUE:
            robot.st_information.light_detection = UNKNOWN_LIGHT_DETECTED #UNKNOWN_LIGHT_DETECTED=0
            error = True
        elif robot.st_data.read_ligth > LIGHT_THRESHOLD:
            robot.st_information.light_detection = HIGH_LIGHT_DETECTED #HIGH_LIGHT_DETECTED=1
        else:
            robot.st_information.light_detection = LOW_LIGHT_DETECTED #LOW_LIGHT_DETECTED=2
    else: #Cualquier otro caso -> ERROR
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
