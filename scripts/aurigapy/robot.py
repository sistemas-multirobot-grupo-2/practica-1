#!/usr/bin/env python3

# Este script contiene la clase robot, que puede tener distintos sensores y controladores

from aurigapy import *
import sensors
import description_constants as constants
import controllers
import time


LEADER_STATE_INFORMATION = constants.MOVING_FORWARD_MAX

##---------------Clases--------------------##
# Este struct contendrá la información de configuración del robot
class Config:
    def __init__(self):
        print("Init Class Config")
        self.max_movement_motors_pwm = 100
        self.min_movement_motors_pwm = 20
        
        self.ultrasonic_sensor_reading_period_in_millis = 150
        
        self.light_threshold_max = 700.0
        self.light_threshold_min = 300.0
        
        self.near_object_threshold  = 15
        self.far_object_threshold   = 75
        
        self.user_interface_refresh_period_in_millis = 500
        
        self.st_config.base_speed = 40.0
        self.st_config.base_turn = 25.0
        
        
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
            self.error = constants.EXECUTION_SUCCESSFUL
            
            self.next_state = constants.STOP 
        
        elif(self.mode == 'simulation'):
            print(self.name + ": Modo de Simulacion")
            self.error = constants.EXECUTION_SUCCESSFUL
            self.next_state = constants.STOP
        
        else:
            print(self.name + ": Modo no reconocido")
            self.error = constants.EXECUTION_ERROR
            self.next_state = constants.EMERGENCY
        
        # Añadimos información de los structs de datos
        self.st_config = Config()
        self.st_meas = sensors.Data() 
        self.st_information = sensors.Information()
        self.st_actions = controllers.Actions()
        
        
        if robot_rol == "leader":
            self.rol = constants.LEADER
        elif robot_rol == "follower":
            self.rol = constants.FOLLOWER
        else:
            self.rol = constants.UNDEFINED
            self.next_state = constants.EMERGENCY
            
        self.list_of_sensors = robot_sensors_list
        self.sensor_ports = robot_sensor_ports_list
        
        # Diccionarios de Sensores
        # Permiten hacer la clase más genérica
        self.READ_SENSORS = {0:""}
        self.PROCESS_SENSORS = {0:""}
        
        self.current_state = self.next_state
        
        
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
    
    def leaderFiniteStateMachine(self):
        """
        Funcion para determinar el siguiente estado del Lider 
        
        :param self: Referencia a la instancia desde la clase
        
        :return: void
        """
        global LEADER_STATE_INFORMATION
        
        if(self.current_state == constants.EMERGENCY or self.current_state == constants.UNDEFINED): # No puede salir de EMERGENCIA, hay que reiniciar el robot
            LEADER_STATE_INFORMATION = self.next_state = constants.EMERGENCY
        #1
        elif(self.current_state == constants.STOP and (self.st_information.light_detection == constants.HIGH_LIGHT_DETECTED or self.st_information.light_detection == constants.LOW_LIGHT_DETECTED or self.st_information.light_detection == constants.UNKNOWN_LIGHT_DETECTED)):
            LEADER_STATE_INFORMATION = self.next_state = constants.STOP
        #2
        elif(self.current_state == constants.MOVING_FORWARD_MAX and (self.st_information.light_detection == constants.NO_LIGHT_DETECTED or self.st_information.light_detection == constants.UNKNOWN_LIGHT_DETECTED)):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_FORWARD_MAX
        #3
        elif(self.current_state == constants.MOVING_FORWARD_PROPORTIONAL and (self.st_information.light_detection == constants.LOW_LIGHT_DETECTED or self.st_information.light_detection == constants.UNKNOWN_LIGHT_DETECTED)):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_FORWARD_PROPORTIONAL
        #4
        elif(self.current_state == constants.MOVING_FORWARD_MAX and self.st_information.light_detection == constants.LOW_LIGHT_DETECTED):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_FORWARD_PROPORTIONAL
            
        #5
        elif(self.current_state == constants.MOVING_FORWARD_PROPORTIONAL and self.st_information.light_detection == constants.NO_LIGHT_DETECTED):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_FORWARD_MAX
            
        #6
        elif(self.current_state == constants.STOP and self.st_information.light_detection == constants.NO_LIGHT_DETECTED and self.st_actions.object_picked == False and self.st_actions.grasping == False):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_FORWARD_MAX
            
        #7
        elif(self.current_state == constants.MOVING_FORWARD_MAX and self.st_information.light_detection == constants.HIGH_LIGHT_DETECTED):
            LEADER_STATE_INFORMATION = self.next_state = constants.STOP
            self.st_actions.grasping = True
            
        #8
        elif(self.current_state == constants.STOP and self.st_information.light_detection == constants.LOW_LIGHT_DETECTED and self.st_actions.object_picked == False and self.st_actions.grasping == False):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_FORWARD_PROPORTIONAL

        #9
        elif(self.current_state == constants.MOVING_FORWARD_PROPORTIONAL and self.st_information.light_detection == constants.HIGH_LIGHT_DETECTED):
            LEADER_STATE_INFORMATION = self.next_state = constants.STOP
            self.st_actions.grasping = True

        #10
        elif(self.current_state == constants.STOP and self.st_information.light_detection == constants.NO_LIGHT_DETECTED and self.st_actions.grasping == True):
            LEADER_STATE_INFORMATION = self.next_state = constants.PICK_PLACE_OBJECT
            self.st_actions.object_picked = not(self.st_actions.object_picked)
            print(self.st_actions.object_picked)

                 
        #11
        #elif(self.current_state == constants.PICK_PLACE_OBJECT and self.st_actions.finished_grasping == False):
        #    self.next_state = constants.PICK_PLACE_OBJECT
            
        #12
        elif(self.current_state == constants.PICK_PLACE_OBJECT and self.st_actions.object_picked == True):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_BACKWARD_MAX
            self.st_actions.grasping = False

        #elif(self.current_state == constants.PICK_PLACE_OBJECT and self.st_actions.object_picked == True and self.st_information.light_detection == constants.NO_LIGHT_DETECTED):
        #    self.next_state = constants.MOVING_BACKWARD_MAX
        #    self.st_actions.grasping = False
        #13
        #elif(self.current_state == constants.PICK_PLACE_OBJECT and self.st_actions.object_picked == True and self.st_information.light_detection == constants.LOW_LIGHT_DETECTED):
        #    self.next_state = constants.MOVING_BACKWARD_PROPORTIONAL
        #    self.st_actions.grasping = False 
        #14
        elif(self.current_state == constants.PICK_PLACE_OBJECT and self.st_actions.object_picked == False):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_FORWARD_MAX
            self.st_actions.grasping = False

        #elif(self.current_state == constants.PICK_PLACE_OBJECT and self.st_actions.object_picked == False and self.st_information.light_detection == constants.NO_LIGHT_DETECTED):
        #    self.next_state = constants.MOVING_FORWARD_MAX
        #    self.st_actions.grasping = False
        #15
        #elif(self.current_state == constants.PICK_PLACE_OBJECT and self.st_actions.object_picked == False and self.st_information.light_detection == constants.LOW_LIGHT_DETECTED):
        #    self.next_state = constants.MOVING_FORWARD_PROPORTIONAL
        #    self.st_actions.grasping = False
        #16
        elif(self.current_state == constants.MOVING_BACKWARD_MAX and (self.st_information.light_detection == constants.NO_LIGHT_DETECTED or self.st_information.light_detection == constants.UNKNOWN_LIGHT_DETECTED)):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_BACKWARD_MAX
        #17
        elif(self.current_state == constants.MOVING_BACKWARD_PROPORTIONAL and (self.st_information.light_detection == constants.LOW_LIGHT_DETECTED or self.st_information.light_detection == constants.UNKNOWN_LIGHT_DETECTED)):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_BACKWARD_PROPORTIONAL
        #18
        elif(self.current_state == constants.MOVING_BACKWARD_MAX and self.st_information.light_detection == constants.LOW_LIGHT_DETECTED):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_BACKWARD_PROPORTIONAL
        #19
        elif(self.current_state == constants.MOVING_BACKWARD_PROPORTIONAL and self.st_information.light_detection == constants.NO_LIGHT_DETECTED):
            LEADER_STATE_INFORMATION = self.next_state = constants.MOVING_BACKWARD_MAX
        #20    
        elif(self.current_state == constants.MOVING_BACKWARD_MAX and self.st_information.light_detection == constants.HIGH_LIGHT_DETECTED):
            LEADER_STATE_INFORMATION = self.next_state = constants.STOP
            self.st_actions.grasping = True
        #21
        elif(self.current_state == constants.MOVING_BACKWARD_PROPORTIONAL and self.st_information.light_detection == constants.HIGH_LIGHT_DETECTED):
            LEADER_STATE_INFORMATION = self.next_state = constants.STOP
            self.st_actions.grasping = True
               
        else:
            LEADER_STATE_INFORMATION = self.next_state = constants.UNDEFINED
            
        self.current_state = self.next_state

    
    # TODO: Cambiar la maquina de estados cuando esten todos los sensores
    def followerFiniteStateMachine(self):
        """
        Funcion para determinar el siguiente estado del Seguidor 
        
        :param self: Referencia a la instancia desde la clase
        
        :return: void
        """
        global LEADER_STATE_INFORMATION
        
        if(self.current_state == constants.EMERGENCY or self.current_state == constants.UNDEFINED): # No puede salir de EMERGENCIA, hay que reiniciar el robot
            self.next_state = constants.EMERGENCY
            
        elif(LEADER_STATE_INFORMATION == constants.EMERGENCY or LEADER_STATE_INFORMATION == constants.UNDEFINED or LEADER_STATE_INFORMATION == constants.STOP or LEADER_STATE_INFORMATION == constants.PICK_PLACE_OBJECT):
            self.next_state = constants.STOP
        
        elif((LEADER_STATE_INFORMATION == constants.MOVING_FORWARD_MAX or LEADER_STATE_INFORMATION == constants.MOVING_FORWARD_PROPORTIONAL) and self.st_information.ultrasensor_detection == constants.COLLISION_OBJECT_DETECTED):
            self.next_state = constants.STOP
            
        elif((LEADER_STATE_INFORMATION == constants.MOVING_FORWARD_MAX or LEADER_STATE_INFORMATION == constants.MOVING_FORWARD_PROPORTIONAL) and self.st_information.ultrasensor_detection == constants.NEAR_OBJECT_DETECTED):
            self.next_state = constants.MOVING_FORWARD_PROPORTIONAL        
        
        elif((LEADER_STATE_INFORMATION == constants.MOVING_FORWARD_MAX or LEADER_STATE_INFORMATION == constants.MOVING_FORWARD_PROPORTIONAL) and self.st_information.ultrasensor_detection == constants.FAR_OBJECT_DETECTED):
            self.next_state = constants.MOVING_FORWARD_MAX
        
        elif((LEADER_STATE_INFORMATION == constants.MOVING_BACKWARD_MAX or LEADER_STATE_INFORMATION == constants.MOVING_BACKWARD_PROPORTIONAL) and self.st_information.ultrasensor_detection == constants.COLLISION_OBJECT_DETECTED):
            self.next_state = constants.MOVING_BACKWARD_MAX
         
        elif((LEADER_STATE_INFORMATION == constants.MOVING_BACKWARD_MAX or LEADER_STATE_INFORMATION == constants.MOVING_BACKWARD_PROPORTIONAL) and self.st_information.ultrasensor_detection == constants.NEAR_OBJECT_DETECTED):
            self.next_state = constants.MOVING_BACKWARD_PROPORTIONAL
        
        elif((LEADER_STATE_INFORMATION == constants.MOVING_BACKWARD_MAX or LEADER_STATE_INFORMATION == constants.MOVING_BACKWARD_PROPORTIONAL) and self.st_information.ultrasensor_detection == constants.FAR_OBJECT_DETECTED):
            self.next_state = constants.STOP
        
        elif(self.current_state == constants.MOVING_FORWARD_MAX and self.st_information.ultrasensor_detection == constants.COLLISION_OBJECT_DETECTED):
            self.next_state = constants.STOP
        
        elif(self.current_state == constants.MOVING_FORWARD_PROPORTIONAL and self.st_information.ultrasensor_detection == constants.COLLISION_OBJECT_DETECTED):
            self.next_state = constants.STOP
            
        elif(self.current_state == constants.MOVING_BACKWARD_MAX and self.st_information.ultrasensor_detection == constants.FAR_OBJECT_DETECTED):
            self.next_state = constants.STOP
        
        elif(self.current_state == constants.MOVING_BACKWARD_PROPORTIONAL and self.st_information.ultrasensor_detection == constants.FAR_OBJECT_DETECTED):
            self.next_state = constants.STOP
        
        elif(self.st_information.ultrasensor_detection == constants.UNKNOWN_OBJECT_DETECTED):
            self.next_state = constants.STOP 
        
        else:
            self.next_state = constants.UNDEFINED  
        
        self.current_state = self.next_state
        
    
    def updateFiniteStateMachine(self):
        """
        Funcion para determinar la maquina de estados a utilizar
        
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        if(self.rol == constants.LEADER):
            self.leaderFiniteStateMachine()
        
        elif(self.rol == constants.FOLLOWER):
            self.followerFiniteStateMachine()
            
        else:
            self.current_state = constants.EMERGENCY               
            
    # TODO: Cambiar el selector del controlador cuando estén los controladores y estados
    def controller(self):
        """
        Función genérica que llama al controlador específico adecuado en función de la tarea
        que se deba realizar.
        
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        if(self.current_state == constants.EMERGENCY or self.current_state == constants.UNDEFINED or constants.STOP):
            controllers.controllerStop(self)
            
        elif(self.current_state == constants.MOVING_FORWARD_MAX):
            controllers.controllerMovingForwardMax(self)

        elif(self.current_state == constants.MOVING_FORWARD_PROPORTIONAL):
            controllers.controllerMovingForwardProportional(self)
            
        elif(self.current_state == constants.MOVING_BACKWARD_MAX):
            controllers.controllerMovingBackwardMax(self)
            
        elif(self.current_state == constants.MOVING_BACKWARD_PROPORTIONAL):
            controllers.controllerMovingBackwardProportional(self)
        
        elif(self.current_state == constants.PICK_PLACE_OBJECT):
            controllers.controllerPickPlace(self) 
        
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
        
        else:
            self.error = constants.EXECUTION_SUCCESSFUL
            
            if(self.current_state == constants.EMERGENCY):
                self.error = constants.EXECUTION_ERROR
            elif(self.current_state == constants.UNDEFINED):
                self.error = constants.EXECUTION_ERROR
            
            else:
                self.mobile_robot.set_command(self.st_actions.command,int(self.st_actions.movement_motors_pwm))

    # TODO: Añadir la info util y cuando esté todo hecho
    def refreshUserInterface (self):
        """
        Función encargada de refrescar la info para el usuario a intervalos de tiempo correctos
        
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        print(self.name + ": Estado: " + str(self.current_state))
        

    def run_main(self):
        """
        Funcion Loop que hace la llamada a todas las funciones de lectura, procesado, maquina de estados,
        control y muestra de datos
         
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        if(self.mode == "real_robot"):
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
                #time.sleep(1) #!!!!!!!!!!!!!!!! ELIMINAR DELAY !!!!!!!!!!!!!!!!#  
    
    
        elif(self.mode == "simulation"):
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
