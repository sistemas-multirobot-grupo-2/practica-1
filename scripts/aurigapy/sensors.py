#!/usr/bin/env python3


from aurigapy import *
import time


# Función específica para leer el sensor de ultrasonidos.    
def readUltraSensor(robot,port):
    if(robot.mode == 'simulation'): 
        print(robot.name + ": Leemos sensor ultrasonidos en el puerto " + str(port))
        

# Función específica para leer el sensor de luz
def readLightSensor(robot,port):
    if(robot.mode == 'simulation'): 
        print(robot.name + ": Leemos sensor de luz en el puerto " + str(port)) 
        
        
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
