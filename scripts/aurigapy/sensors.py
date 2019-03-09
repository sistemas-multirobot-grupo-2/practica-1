#!/usr/bin/env python3


## Este script se encarga de recoger las funciones que engloban la lectura y procesado de los datos

import description_constants as constants
from aurigapy import *
import time

#TODO: Añadir las funiones que vayan haciendo yoinel y josemi
#Todo lo que hay hasta el momento son EJEMPLOS (cambiad lo que os parezca)



# Este struct contendrá la información raw de los sensores
class Data:
    def __init__(self):
        print("Init Class Data")
        self.ultrasensor_distance = constants.IMPOSSIBLE_DISTANCE #Distancia en cm leida por el sensor de distancia. "-1" para UNKNOWN
        self.light_sensor_value = constants.IMPOSSIBLE_LIGHT_VALUE #Valor entre 0 y 1024 de intensidad de luz. "-1" para UNKNOWN
        self.line_detection = constants.UNKNOWN_LINE_VALUE #0-los 2 on; 1-izq on; 2-der on; 3-ninguno. "-1" para UNKNOWN
        
# Este struct contendrá la información procesada de los sensores
class Information:
    def __init__(self):
        print("Init Class Information")
        self.ultrasensor_detection = constants.NO_OBJECT_DETECTED #Posicion de un posible objeto (NEAR, FAR, NO)
        self.light_detection = constants.UNKNOWN_LIGHT_DETECTED #Posicion de un posible objeto (HIGH, LOW, UNKNOWN)
        
        
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
            
            if(robot.st_meas.ultrasensor_distance < constants.MIN_ULTRASONIC_VALUE or robot.st_meas.ultrasensor_distance > constants.MAX_ULTRASONIC_VALUE):
                robot.st_meas.ultrasensor_distance = constants.IMPOSSIBLE_DISTANCE
            
        else:
            robot.st_meas.ultrasensor_distance = constants.IMPOSSIBLE_DISTANCE
            error = True #Indicar error porque NO se ha podido leer la distancia (ha pasado demasiado poco tiempo)
    else: #Cualquier otro caso -> ERROR
        robot.st_meas.ultrasensor_distance = constants.IMPOSSIBLE_DISTANCE
        error = True
        
    print("[*] Dato de distancia: " + str(robot.st_meas.ultrasensor_distance))
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
        robot.st_meas.light_sensor_value = robot.mobile_robot.get_light_sensor_onboard(port) #Leer datos del sensor
        print("[*] Dato de luz raw: " + str(robot.st_meas.light_sensor_value))
        # sensor si la lectura da un valor ilogico
        if(robot.st_meas.light_sensor_value < constants.MIN_LIGHT_VALUE or robot.st_meas.light_sensor_value > constants.MAX_LIGHT_VALUE):
            robot.st_meas.light_sensor_value = constants.IMPOSSIBLE_LIGHT_VALUE
            error = True
            
    else: #Cualquier otro caso -> ERROR
        robot.st_meas.light_sensor_value = constants.IMPOSSIBLE_LIGHT_VALUE
        error = True
        
    print("[*] Dato de luz: " + str(robot.st_meas.light_sensor_value))
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
        robot.st_meas.line_detection = robot.mobile_robot.get_line_sensor(port) #Leer informacion -> 0-los 2 on; 1-izq on; 2-der on; 3-ninguno    
        
        #Si se recibe un valor no-valido
        if robot.st_meas.line_detection<0 or robot.st_meas.line_detection>3:
            robot.st_meas.line_detection = constants.UNKNOWN_LINE_VALUE
            error = True #Indicar fallo
            
    else: #Cualquier otro caso -> ERROR
        robot.st_meas.line_detection = constants.UNKNOWN_LINE_VALUE
        error = True
        
    print("[*] Dato de linea: " + str(robot.st_meas.line_detection))
    return error #Devolver la variable que indica si ha habido algun fallo
                

##------------------Procesado------------------##  
#PROCESADO A ALTO NIVEL PARA OBTENER COMPORTAMIENTO DEL LIDER
def deltaDistance(self):
        """Funcion que devuelve el incremento de distancia en el ultrasonidos en funcion de si es positiva o negativa"""
        self.followerLastKnownDistance = self.followerLastKnownDistance - self.st_information.ultrasensor_detection
        if(self.followerLastKnownDistance > constants.U_S_MARGIN):
            print("Following leader")
            return constants.FOLLOW
        elif(self.followerLastKnownDistance < constants.U_S_MARGIN):
            print("Repelling leader")
            return constants.REPELL
        else:
            print("Waiting for leader to move")
            return constants.WAIT

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
        if(robot.st_meas.ultrasensor_distance == constants.IMPOSSIBLE_DISTANCE):
           robot.st_information.ultrasensor_detection = constants.UNKNOWN_OBJECT_DETECTED
           error = True
  
        elif(robot.st_meas.ultrasensor_distance < robot.st_config.near_object_threshold):
            robot.st_information.ultrasensor_detection = constants.NO_OBJECT_DETECTED 
        
        elif(robot.st_meas.ultrasensor_distance > robot.st_config.near_object_threshold and robot.st_meas.ultrasensor_distance < robot.st_config.far_object_threshold):
            robot.st_information.ultrasensor_detection = constants.NEAR_OBJECT_DETECTED 
        
        elif(robot.st_meas.ultrasensor_distance > robot.st_config.far_object_threshold):
            robot.st_information.ultrasensor_detection = constants.FAR_OBJECT_DETECTED
        else:
            robot.st_information.ultrasensor_detection = constants.UNKNOWN_OBJECT_DETECTED 
    
    else: #Cualquier otro caso -> ERROR
        error = True
        robot.st_information.ultrasensor_detection = constants.UNKNOWN_OBJECT_DETECTED
        
    print("[*] Procesado de distancia: " + str(robot.st_information.ultrasensor_detection))
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
        
        if(robot.st_meas.light_sensor_value == constants.IMPOSSIBLE_LIGHT_VALUE):
            robot.st_information.light_detection = constants.UNKNOWN_LIGHT_DETECTED #UNKNOWN_LIGHT_DETECTED=0
            error = True
        
        elif(robot.st_meas.light_sensor_value > robot.st_config.light_threshold_max):
            robot.st_information.light_detection = constants.HIGH_LIGHT_DETECTED #HIGH_LIGHT_DETECTED=1
        
        elif(robot.st_meas.light_sensor_value > robot.st_config.light_threshold_min and robot.st_meas.light_sensor_value < robot.st_config.light_threshold_max):
            robot.st_information.light_detection = constants.LOW_LIGHT_DETECTED #LOW_LIGHT_DETECTED=2
        
        elif(robot.st_meas.light_sensor_value < robot.st_config.light_threshold_min):
            robot.st_information.light_detection = constants.NO_LIGHT_DETECTED 
        
        else: #Cualquier otro caso -> ERROR
            robot.st_information.light_detection = constants.UNKNOWN_LIGHT_DETECTED
            error = True
            
    else: #Cualquier otro caso -> ERROR
        robot.st_information.light_detection = constants.UNKNOWN_LIGHT_DETECTED
        error = True
        
    print("[*] Procesado de luz: " + str(robot.st_information.light_detection))
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
