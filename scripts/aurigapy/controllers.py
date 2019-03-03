#!/usr/bin/env python3


## Este script se encarga de recoger los controladores

from aurigapy import *
import time

#TODO: Añadir las funiones que vayan haciendo paco y abel

# Este struct contendrá las salidas que hay que aplicar a cada motor
class Actions:
    def __init__(self):
        print("Init Class Actions")

# Controlador específico para parar motores
def controllerStop(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control")
