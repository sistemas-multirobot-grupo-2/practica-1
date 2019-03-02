#!/usr/bin/env python3


from aurigapy import *
import time

# Este struct contendrá la información de configuración del robot
class Config:
    def __init__(self):
        print("Init Class")

# Este struct contendrá la información raw de los sensores
class Data:
    def __init__(self):
        print("Init Class")

# Este struct contendrá la información procesada de los sensores
class Information:
    def __init__(self):
        print("Init Class")
        
# Este struct contendrá las salidas que hay que aplicar a cada motor
class Actions:
    def __init__(self):
        print("Init Class")
        
# Clase robot
class Robot:
    def __init__(self,bluetooth_path):
        print("Init Class")
        
        
    # Función específica para leer el sensor de ultrasonidos.    
    def readUltraSensor(self):
        print("Leemos sensor ultrasonidos") 
    
    
    # Función genérica que debe ir llamando a cada una de las funciones específicas para rellenar el struct de "Data" con 
    # los datos de todos los sensores instalados.
    def readSensors(self):
        self.readUltraSensor()
  
    # Procesador específico para extaer información acerca de la presencia de obstáculos en base a los datos del 
    # sensor de ultrasonidos.
    def processUltrasonicSensorData(self):
        print("Procesamos la información del sensor de ultrasonidos")
    
    # Función para extraer la información a partir de los datos 'en crudo'.
    def processData(self):
        self.processUltrasonicSensorData()

    # Función para determinar qué tarea se va a llevar a cabo a partir de la información extraída a partir
    # de los datos de los sensores. 
    def updateFiniteStateMachine(self):
        print("Actualizamos la maquina de estados")

    # Controlador específico para parar motores
    def controllerStop(self):
        print("Calculamos la acción de control")

    # Función genérica que llama al controlador específico adecuado en función de la tarea
    # que se deba realizar. 
    def controller(self):
        self.controllerStop()         

    # Función encargada de pasar a motores los comandos calculados por los controladores
    # este es el último punto antes de actuar sobre los motores,por lo que tenemos que 
    # ser cuidadosos de no enviar valores indeseados... En este caso la máquina es pequeña
    # pero imaginemos que vamos a acelerar un coche o un camión... hay que pensar bien
    # antes de actuar!!
    def execute(self):
        print("Mandamos la acción de control a los actuadores")

    # Función encargada de refrescar la info para el usuario a intervalos de tiempo correctos
    def refreshUserInterface (self):
        print("Mostramos la informacion util y los errores")

    
    def run_main(self):
        while True:
            # Leemos los sensores
            self.readSensors()
            
            # Extraemos la información a partir de los datos
            self.processData()
            
            # Actualizamos la máquina de estados a partir de la información recibida por los sensores 
            self.updateFiniteStateMachine()
           
            # Calculamos las acciones que tenemos que aplicar a los distintos motores, en función del
            # estado y las lecturas de los sensores
            self.controller()
            
            # Pasamos a motores las acciones calculadas
            self.execute()

            # Publicamos info importante para el debug
            self.refreshUserInterface()
            
            time.sleep(2)
            
        

