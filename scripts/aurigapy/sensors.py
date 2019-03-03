#!/usr/bin/env python3


## Este script se encarga de recoger las funciones que engloban la lectura y procesado de los datos


from aurigapy import *
import time

#TODO: Añadir las funiones que vayan haciendo yoinel y josemi

# Este struct contendrá la información raw de los sensores
class Data:
    def __init__(self):
        print("Init Class Data")

# Este struct contendrá la información procesada de los sensores
class Information:
    def __init__(self):
        print("Init Class Information")
        

##------------------Lectura------------------##        

# Función específica para leer el sensor de ultrasonidos.    
def readUltraSensor(robot,port):
    if(robot.mode == 'simulation'): 
        print(robot.name + ": Leemos sensor ultrasonidos en el puerto " + str(port))
        

# Función específica para leer el sensor de luz
def readLightSensor(robot,port):
    if(robot.mode == 'simulation'): 
        print(robot.name + ": Leemos sensor de luz en el puerto " + str(port)) 

# Función específica para leer el sensor de linea
def readLineSensor(robot,port):
    if(robot.mode == 'simulation'): 
        print(robot.name + ": Leemos sensor de linea en el puerto " + str(port)) 
                

##------------------Procesado------------------##  
      
# Procesador específico para extaer información acerca de la presencia de obstáculos en base a los datos del 
# sensor de ultrasonidos.
def processUltrasonicSensorData(robot,port):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Procesamos la información del sensor de ultrasonidos en el puerto " + str(port))
        
# Procesador específico para extaer información acerca de la presencia de una fuente lumínica en base a los datos del 
# sensor de luz.
def processLightSensorData(robot,port):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Procesamos la información del sensor de luz en el puerto " + str(port))

# Procesador específico para extaer información acerca de la presencia de una linea.
def processLineSensorData(robot,port):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Procesamos la información del sensor de linea en el puerto " + str(port))
