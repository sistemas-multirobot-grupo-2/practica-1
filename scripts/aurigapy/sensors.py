#!/usr/bin/env python3


## Este script se encarga de recoger las funciones que engloban la lectura y procesado de los datos


from aurigapy import *
import time

#TODO: Añadir las funiones que vayan haciendo yoinel y josemi
#Todo lo que hay hasta el momento son EJEMPLOS (cambiad lo que os parezca)


##-----Constantes y variables globales-----##

#Ultrasonidos
IMPOSSIBLE_DISTANCE = -1.0


# Este struct contendrá la información raw de los sensores
class Data:
    def __init__(self):
        print("Init Class Data")
        self.ultrasensor_distance = -1 #Distancia en cm leida por el sensor de distancia. "-1" para UNKNOWN
        self.read_light = -1 #Valor entre 0 y 1024 de intensidad de luz. "-1" para UNKNOWN
        self.line_detection = -1 #0-los 2 on; 1-izq on; 2-der on; 3-ninguno. "-1" para UNKNOWN

# Este struct contendrá la información procesada de los sensores
class Information:
    def __init__(self):
        print("Init Class Information")
        
##------------------Lectura------------------##        

# Función específica para leer el sensor de ultrasonidos.    
def readUltraSensor(robot,port):
    if(robot.mode == 'simulation'): 
        print(robot.name + ": Leemos sensor ultrasonidos en el puerto " + str(port))
    
    elif(robot.mode == 'real_robot'):
        robot.st_data.ultrasensor_distance = robot.mobile_robot.get_ultrasonic_reading(port)
    
    else:
        robot.st_data.ultrasensor_distance = IMPOSSIBLE_DISTANCE
        

# Función específica para leer el sensor de luz
def readLightSensor(robot,port):
"""
Funcion para leer el sensor de luz

:param self: Referencia a la instancia desde la que se llama a la funcion
:param port: Puerto donde esta conectado el sensor de luz.

:return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
"""
    error = False #Variable que contiene el valor de retorno
    
    if robot.mode == 'simulation':
        print(robot.name + ": Procesamos la información del sensor de luz en el puerto " + str(port))
    else:
        robot.st_data.read_ligth = robot.get_light_sensor_onboard(port) #Leer datos del sensor

        #Comprobar si la lectura da un valor logico
        if robot.st_data.read_ligth<1 or robot.st_data.read_ligth>1023:
            error = True
    
    return error


# Función específica para leer el sensor de linea
def readLineSensor(robot,port):
"""
Funcion para leer el sensor de linea

:param robot: Referencia a la instancia desde la que se llama a la funcion
:param port: Puerto donde esta conectado el sensor de linea.

:return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
"""
    error = False #Variable que contiene el valor de retorno
    
    if robot.mode == 'simulation':
        print(robot.name + ": Procesamos la información del sensor de linea en el puerto " + str(port))
    else: 
        robot.st_data.line_detection = robot.get_line_sensor(port) #Leer informacion -> 0-los 2 on; 1-izq on; 2-der on; 3-ninguno
        
        #Si se recibe un valor no-valido
        if robot.st_data.line_detection<0 or robot.st_data.line_detection>3:
            error = True #Indicar fallo
        
        return error #Devolver la variable que indica si ha habido algun fallo
                

##------------------Procesado------------------##  
      
# Procesador específico para extaer información acerca de la presencia de obstáculos en base a los datos del 
# sensor de ultrasonidos.
def processUltrasonicSensorData(robot,port):
"""
Funcion para extaer informacion acerca de la presencia de obstaculos en base a los datos del sensor de distancia (ultrasonidos)

:param self: Referencia a la instancia desde la que se llama a la funcion
:param port: Puerto donde esta conectado el sensor de distancia (ultrasonidos).

:return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
"""
    if robot.mode == 'simulation':
        print(robot.name + ": Procesamos la información del sensor de ultrasonidos en el puerto " + str(port))
        
    
# Procesador específico para extaer información acerca de la presencia de una fuente lumínica en base a los datos del 
# sensor de luz.
def processLightSensorData(robot,port):
"""
Funcion para extaer informacion acerca de la presencia de obstaculos en base a los datos del sensor de luz

:param self: Referencia a la instancia desde la que se llama a la funcion
:param port: Puerto donde esta conectado el sensor de luz.

:return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
"""
    if robot.mode == 'simulation':
        print(robot.name + ": Procesamos la información del sensor de luz en el puerto " + str(port))

        
# Procesador específico para extaer información acerca de la presencia de una linea.
def processLineSensorData(robot,port):
"""
Funcion para extaer informacion acerca de la presencia de obstaculos en base a los datos del sensor de linea

:param robot: Referencia a la instancia desde la que se llama a la funcion
:param port: Puerto donde esta conectado el sensor de linea.

:return: True si no ha habido ningun problema. False en cualquier otro caso (ERROR)
"""
    if robot.mode == 'simulation':
        print(robot.name + ": Procesamos la información del sensor de linea en el puerto " + str(port))
