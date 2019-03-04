#!/usr/bin/env python3

# Este script contiene la clase robot, que puede tener distintos sensores y controladores

from aurigapy import *
import sensors
import controllers
import time

##-----Constantes y variables globales-----##

# Estados
STOP                              =  0
MOVING_FORWARD_MAX                =  1
MOVING_FORWARD_PROPORTIONAL       =  2
MOVING_BACKWARD_MAX               =  3
MOVING_BACKWARD_PROPORTIONAL      =  4
PICK_OBJECT                       =  5
EMERGENCY                         = -1
UNDEFINED                         = -2


# Codigos de Error
EXECUTION_ERROR         = -1
EXECUTION_SUCCESSFUL    =  0

# Roles
LEADER      =  0
FOLLOWER    =  1
UNDEFINED   = -1


##---------------Clases--------------------##
# Este struct contendrá la información de configuración del robot
class Config:
    def __init__(self):
        print("Init Class Config")
        self.max_movement_motors_pwm = 255
        self.ultrasonic_sensor_reading_period_in_millis = 150
        self.user_interface_refresh_period_in_millis = 500
        
# Clase robot
class Robot:
    def __init__(self,name,mode,bluetooth_path,robot_rol,robot_sensors_list,robot_sensor_ports_list):
        print("Init Class Robot")
        
        self.name = name
        self.mode = mode
        
        
        if(self.mode == 'real_robot'):
            print(self.name + ": Modo usando el Robot real")
            self.mobile_robot = AurigaPy(debug=False)
            self.mobile_robot.connect(bluetooth_path)
            self.error = EXECUTION_SUCCESSFUL
            self.state = STOP
        
        elif(self.mode == 'simulation'):
            print(self.name + ": Modo de Simulacion")
            self.error = EXECUTION_SUCCESSFUL
            self.state = STOP
        
        else:
            print(self.name + ": Modo no reconocido")
            self.error = EXECUTION_ERROR
            self.state = EMERGENCY
        
        # Añadimos información de los structs de datos
        self.st_config = Config()
        self.st_meas = sensors.Data() 
        self.st_information = sensors.Information()
        self.st_actions = controllers.Actions()
        
        
        if robot_rol == "leader":
            self.rol = LEADER
        elif robot_rol == "follower":
            self.rol = FOLLOWER
        else:
            self.rol = UNDEFINED
            self.state = EMERGENCY
            
        self.list_of_sensors = robot_sensors_list
        self.sensor_ports = robot_sensor_ports_list
        
        # Diccionarios de Sensores
        # Permiten hacer la clase más genérica
        self.READ_SENSORS = {0:""}
        self.PROCESS_SENSORS = {0:""}
        

    # TODO: Añadir elementos cuando esten todos los sensores
    def addSensors(self):
        """
        Funcion para añadir los sensores del robot

        :param self: Referencia a la instancia desde la clase
        
        :return: void
        """
        count = 0
        for sensor in self.list_of_sensors:
            if(sensor == "ultrasonic"):
                self.READ_SENSORS[count] = sensors.readUltraSensor
                self.PROCESS_SENSORS[count] = sensors.processUltrasonicSensorData
                print(self.name +": Add " + sensor + " sensor, port: " + str(self.sensor_ports[count]))
                count += 1
            elif(sensor == "light"):
                self.READ_SENSORS[count] = sensors.readLightSensor
                self.PROCESS_SENSORS[count] = sensors.processLightSensorData
                print(self.name +": Add " + sensor + " sensor, port: " + str(self.sensor_ports[count]))
                count += 1
            elif(sensor == "line"):
                self.READ_SENSORS[count] = sensors.readLineSensor
                self.PROCESS_SENSORS[count] = sensors.processLineSensorData
                print(self.name +": Add " + sensor + " sensor, port: " + str(self.sensor_ports[count]))
                count += 1
                
    def readSensors(self):
        """
        Función genérica que debe ir llamando a cada una de las funciones específicas para rellenar el struct de "Data" con 
        los datos de todos los sensores instalados.
        
        :param self: Referencia a la instancia desde la clase
        
        :return: void
        """
        for sensor in self.READ_SENSORS:
            self.READ_SENSORS[sensor](self,self.sensor_ports[sensor])

    def processData(self):
        """
        Función genérica que debe ir llamando a cada una de las funciones específicas 
        para extraer la información a partir de los datos 'en crudo'.
        
        :param self: Referencia a la instancia desde la clase
        
        :return: void
        """
        for sensor in self.PROCESS_SENSORS:
            self.PROCESS_SENSORS[sensor](self,self.sensor_ports[sensor])
    
    # TODO: Cambiar la maquina de estados cuando esten todos los sensores
    def leaderFiniteStateMachine(self):
        """
        Funcion para determinar el siguiente estado del Lider 
        
        :param self: Referencia a la instancia desde la clase
        
        :return: void
        """
        print(self.name + ": Actualizamos la maquina de estado del lider")
        
        if(self.st_meas):
            self.state = STOP
            
        elif(self.st_meas):
            self.state = MOVING_FORWARD_MAX
            
        elif(self.st_meas):
            self.state = MOVING_FORWARD_PROPORTIONAL
        
        elif(self.st_meas):
            self.state = MOVING_BACKWARD_MAX    
            
        elif(self.st_meas):
            self.state = MOVING_BACKWARD_PROPORTIONAL    
            
        elif(self.st_meas):
            self.state = PICK_OBJECT
        
        elif(self.st_meas):
            self.state = EMERGENCY
            
        else:
            self.state = UNDEFINED
    
    # TODO: Cambiar la maquina de estados cuando esten todos los sensores
    def followerFiniteStateMachine(self):
        """
        Funcion para determinar el siguiente estado del Seguidor 
        
        :param self: Referencia a la instancia desde la clase
        
        :return: void
        """
        print(self.name + ": Actualizamos la maquina de estados del seguidor")
        
        if(self.st_meas):
            self.state = STOP
            
        elif(self.st_meas):
            self.state = MOVING_FORWARD_MAX
            
        elif(self.st_meas):
            self.state = MOVING_FORWARD_PROPORTIONAL
        
        elif(self.st_meas):
            self.state = MOVING_BACKWARD_MAX    
            
        elif(self.st_meas):
            self.state = MOVING_BACKWARD_PROPORTIONAL    
            
        elif(self.st_meas):
            self.state = PICK_OBJECT
        
        elif(self.st_meas):
            self.state = EMERGENCY
            
        else:
            self.state = UNDEFINED
    
    def updateFiniteStateMachine(self):
        """
        Funcion para determinar la maquina de estados a utilizar
        
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        if(self.rol == LEADER):
            self.leaderFiniteStateMachine()
        
        elif(self.rol == FOLLOWER):
            self.followerFiniteStateMachine()
            
        else:
            self.state = EMERGENCY               
            
    # TODO: Cambiar el selector del controlador cuando estén los controladores y estados
    def controller(self):
        """
        Función genérica que llama al controlador específico adecuado en función de la tarea
        que se deba realizar.
        
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        if(self.state == STOP):
            controllers.controllerStop(self)
            
        elif(self.state == MOVING_FORWARD_MAX):
            controllers.controllerStop(self)

        elif(self.state == MOVING_FORWARD_PROPORTIONAL):
            controllers.controllerStop(self)
            
        elif(self.state == MOVING_BACKWARD_MAX):
            controllers.controllerStop(self)
            
        elif(self.state == MOVING_BACKWARD_PROPORTIONAL):
            controllers.controllerStop(self)
        
        elif(self.state == PICK_OBJECT):
            controllers.controllerStop(self)
        
        elif(self.state == EMERGENCY):
            controllers.controllerStop(self)
            
        elif(self.state == UNDEFINED):
            controllers.controllerStop(self)
        
        else:
            controllers.controllerStop(self)       

    # TODO: Añadir cuando esten hechos los controladores
    def execute(self):
        """
        Función encargada de pasar a motores los comandos calculados por los controladores
        este es el último punto antes de actuar sobre los motores,por lo que tenemos que
        ser cuidadosos de no enviar valores indeseados
        
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        if(self.mode == 'simulation'):
            print(self.name + ": Mandamos la acción de control a los actuadores")
        
        self.error = EXECUTION_SUCCESSFUL
        
        if(self.state == EMERGENCY):
            self.error = EXECUTION_ERROR
        elif(self.state == UNDEFINED):
            self.error = EXECUTION_ERROR

    # TODO: Añadir la info util y cuando esté todo hecho
    def refreshUserInterface (self):
        """
        Función encargada de refrescar la info para el usuario a intervalos de tiempo correctos
        
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        if(self.mode == 'simulation'):
            print(self.name + ": Mostramos la informacion util y los errores")

    def run_main(self):
        """
        Funcion Loop que hace la llamada a todas las funciones de lectura, procesado, maquina de estados,
        control y muestra de datos
         
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        self.addSensors()
        
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
            
            print(self.name + ": --------------------------")
            time.sleep(2) #!!!!!!!!!!!!!!!! ELIMINAR DELAY !!!!!!!!!!!!!!!!#  
        
