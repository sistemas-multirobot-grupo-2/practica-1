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
PICK_PLACE_OBJECT                       =  5
UNDEFINED                         = -1
EMERGENCY                         = -2

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
            self.next_state = STOP 
        
        elif(self.mode == 'simulation'):
            print(self.name + ": Modo de Simulacion")
            self.error = EXECUTION_SUCCESSFUL
            self.next_state = STOP
        
        else:
            print(self.name + ": Modo no reconocido")
            self.error = EXECUTION_ERROR
            self.next_state = EMERGENCY
        
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
            self.next_state = EMERGENCY
            
        self.list_of_sensors = robot_sensors_list
        self.sensor_ports = robot_sensor_ports_list
        
        # Diccionarios de Sensores
        # Permiten hacer la clase más genérica
        self.READ_SENSORS = {0:""}
        self.PROCESS_SENSORS = {0:""}
        
        self.current_state = self.next_state
        

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
        if(self.mode == 'simulation'):
            print(self.name + ": Actualizamos la maquina de estado del lider")
         
        else:
            if(self.current_state == EMERGENCY or self.current_state == UNDEFINED): # No puede salir de EMERGENCIA, hay que reiniciar el robot
                self.next_state = EMERGENCY
            
            elif(self.current_state == STOP and (self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED or self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = STOP
            
            elif(self.current_state == MOVING_FORWARD_MAX and (self.st_information.light_detection == sensors.NO_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = MOVING_FORWARD_MAX
            
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and (self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = MOVING_FORWARD_PROPORTIONAL
            
            elif(self.current_state == MOVING_FORWARD_MAX and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED):
                self.next_state = MOVING_FORWARD_PROPORTIONAL
            
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED):
                self.next_state = MOVING_FORWARD_MAX
            
            elif(self.currect_state == STOP and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED and self.st_actions.object_picked == False):
                self.next_state = MOVING_FORWARD_MAX    
            
            elif(self.current_state == MOVING_FORWARD_MAX and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
            
            elif(self.currect_state == STOP and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED and self.st_actions.object_picked == False):
                self.next_state = MOVING_FORWARD_PROPORTIONAL    
            
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
            
            elif(self.currect_state == STOP and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED):
                self.next_state = PICK_PLACE_OBJECT
                self.st_actions.object_picked = ~self.st_actions.object_picked     
            
            elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.finished_grasping == False):
                self.next_state = PICK_PLACE_OBJECT
            
            elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.finished_grasping == True and self.st_actions.object_picked == True and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED):
                self.next_state = MOVING_BACKWARD_MAX
            
            elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.finished_grasping == True and self.st_actions.object_picked == True and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED):
                self.next_state = MOVING_BACKWARD_PROPORTIONAL 
            
            elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.finished_grasping == True and self.st_actions.object_picked == False and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED):
                self.next_state = MOVING_FORWARD_MAX
            
            elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.finished_grasping == True and self.st_actions.object_picked == False and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED):
                self.next_state = MOVING_FORWARD_PROPORTIONAL
            
            elif(self.current_state == MOVING_BACKWARD_MAX and (self.st_information.light_detection == sensors.NO_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = MOVING_BACKWARD_MAX
            
            elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL and (self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = MOVING_BACKWARD_PROPORTIONAL
            
            elif(self.current_state == MOVING_BACKWARD_MAX and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED):
                self.next_state = MOVING_BACKWARD_PROPORTIONAL
            
            elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED):
                self.next_state = MOVING_BACKWARD_MAX
                
            elif(self.current_state == MOVING_BACKWARD_MAX and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
            
            elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
                    
            else:
                self.next_state = UNDEFINED
                
            self.current_state = self.next_state
            
            
            
                
            #----------------------ANTIGUA---------------------#
            """elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
            
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
                
            elif(self.current_state == STOP and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = PICK_PLACE_OBJECT
            
            elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.finish_picking == False):
                self.next_state = PICK_PLACE_OBJECT
            
            elif(self.self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED and controllers.st_actions.command == FORWARD):
                self.next_state = MOVING_FORWARD_PROPORTIONAL
            
            elif(self.self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED and controllers.st_actions.command == BACKWARD):
                self.next_state = MOVING_BACKWARD_PROPORTIONAL
            
            elif(self.self.st_information.light_detection == sensors.NO_LIGHT_DETECTED and controllers.st_actions.command == FORWARD):
                self.next_state = MOVING_FORWARD_MAX
            
            elif(self.self.st_information.light_detection == sensors.NO_LIGHT_DETECTED and controllers.st_actions.command == BACKWARD):
                self.next_state = MOVING_BACKWARD_MAX
            
            else:
                self.next_state = UNDEFINED"""
        
        
        """elif(self.st_meas): #STOP
            self.next_state = STOP
            # Detectar objetivo a mover/obstáculo
            # Follower nos pierde
            # Emergencia
            # if(self.READ_SENSOR[ultrasonidos y luz] == objeto_a_distancia_casi_nula or Follower_signal = 0 or parada_emergencia): #STOP
        
        elif(self.st_meas):#MOVING_FORWARD_MAX
            self.state = MOVING_FORWARD_MAX
            # Movemos motores al máx (Se supone que no saliéndose de la línea y lo hace moving)
            # Comprobamos que estamos rectos
                
        elif(self.st_meas):#MOVING_FORWARD_PROPORTIONAL
            self.state = MOVING_FORWARD_PROPORTIONAL
            # Nos movemos adecuando la velocidad para llegar frenando
            # Activamos si nos salimos de una curva (creo que auto)
            # if(self.READ_SENSOR[ultrasonidos/luz] == objeto_a_distancia):
        elif(self.st_meas):#MOVING_BACKWARD_MAX    
            self.state = MOVING_BACKWARD_MAX    
            # Movemos motores al máx (Se supone que no saliéndose de la línea)
            # Comprobamos que estamos rectos
            # Activamos si hay obstáculo inesperado?
            # if(self.READ_SENSOR[pinza/ultrasonidos] == objeto_cogido and luz_de_cogida):

        elif(self.st_meas):#MOVING_BACKWARD_PROPORTIONAL
            self.state = MOVING_BACKWARD_PROPORTIONAL    
            # Nos movemos adecuando la velocidad para llegar frenando atrás
            # Activamos si nos salimos de una curva/necesitamos ir hacia atrás o acercarnos al esclavo
        elif(self.st_meas):#PICK_PLACE_OBJECT
            self.state = PICK_PLACE_OBJECT
            # Detectamos objeto a dist segura y no nos movemos
            # Avanzamos hasta el objeto y cerramos pinza
            # if(self.READ_SENSOR[ultrasonidos/luz] == objeto_a_distancia_nula and orden_de_coger):

        elif(self.st_meas):#EMERGENCY
            self.state = EMERGENCY
            # Objeto que no es objetivo
            # perdemos señal de esclavo
            # no encontramos línea
            # if(self.READ_SENSOR[lineas] == ninguna_linea or slave_offline):
        """

    
    # TODO: Cambiar la maquina de estados cuando esten todos los sensores
    def followerFiniteStateMachine(self):
        """
        Funcion para determinar el siguiente estado del Seguidor 
        
        :param self: Referencia a la instancia desde la clase
        
        :return: void
        """
        print(self.name + ": Actualizamos la maquina de estados del seguidor")
        
        """if(self.st_meas): #STOP
            self.state = STOP
            # Detectar objetivo a mover/obstáculo del lider detectado
            # Emergencia
        elif(self.st_meas):#MOVING_FORWARD_MAX
            self.state = MOVING_FORWARD_MAX
            # Movemos motores al máx (Se supone que no saliéndose de la línea)
            # Comprobamos que estamos rectos
            # Estamos siguiendo al lider
        elif(self.st_meas):#MOVING_FORWARD_PROPORTIONAL
            self.state = MOVING_FORWARD_PROPORTIONAL
            # Nos movemos adecuando la velocidad para llegar frenando
            # Activamos si nos salimos de una curva
            # Estamos siguiendo al lider
            # Muy cerca del lider
        elif(self.st_meas):#MOVING_BACKWARD_MAX    
            self.state = MOVING_BACKWARD_MAX    
            # Movemos motores al máx (Se supone que no saliéndose de la línea)
            # Comprobamos que estamos rectos
            # Activamos si hay obstáculo inesperado
            # Estamos siguiendo al lider y se acerca a nosotros
        elif(self.st_meas):#MOVING_BACKWARD_PROPORTIONAL
            self.state = MOVING_BACKWARD_PROPORTIONAL    
            # Nos movemos adecuando la velocidad para llegar frenando
            # Activamos si nos salimos de una curva/necesitamos ir hacia atrás o el lider hace eso
        elif(self.st_meas):#PICK_PLACE_OBJECT NO EXISTE
            self.state = PICK_PLACE_OBJECT
        elif(self.st_meas):#EMERGENCY
            self.state = EMERGENCY
            # Objeto que no es objetivo
            # perdemos señal del lider
            # no encontramos línea
            # no detectamos al lider
            
        else: #ERROR
            self.state = UNDEFINED"""
    
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
            self.current_state = EMERGENCY               
            
    # TODO: Cambiar el selector del controlador cuando estén los controladores y estados
    def controller(self):
        """
        Función genérica que llama al controlador específico adecuado en función de la tarea
        que se deba realizar.
        
        :param self: Referencia a la instancia desde la clase
        
        :return void
        """
        if(self.current_state == STOP):
            controllers.controllerStop(self)
            
        elif(self.current_state == MOVING_FORWARD_MAX):
            controllers.controllerStop(self)

        elif(self.stcurrent_stateate == MOVING_FORWARD_PROPORTIONAL):
            controllers.controllerStop(self)
            
        elif(self.current_state == MOVING_BACKWARD_MAX):
            controllers.controllerStop(self)
            
        elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL):
            controllers.controllerStop(self)
        
        elif(self.current_state == PICK_PLACE_OBJECT):
            controllers.controllerStop(self)
        
        elif(self.current_state == EMERGENCY):
            controllers.controllerStop(self)
            
        elif(self.current_state == UNDEFINED):
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
        
        if(self.current_state == EMERGENCY):
            self.error = EXECUTION_ERROR
        elif(self.current_state == UNDEFINED):
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
        
