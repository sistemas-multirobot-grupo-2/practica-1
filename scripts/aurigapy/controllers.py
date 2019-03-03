#!/usr/bin/env python3


## Este script se encarga de recoger los controladores

from aurigapy import *
import time


# Controlador específico para parar motores
def controllerStop(robot):
    if(robot.mode == 'simulation'):
        print(robot.name + ": Calculamos la acción de control")
