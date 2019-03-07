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
PICK_PLACE_OBJECT                 =  5
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
        self.max_movement_motors_pwm = 100
        self.min_movement_motors_pwm = 20

        self.ultrasonic_sensor_reading_period_in_millis = 150

        self.light_threshold_max = 700
        self.light_threshold_min = 300

        self.near_object_threshold  = 10
        self.far_object_threshold   = 250

        self.user_interface_refresh_period_in_millis = 500

        self.distance_change = 1

# Clase robot
class Robot:
    def __init__(self,name,mode,bluetooth_path,robot_rol,robot_sensors_list,robot_sensor_ports_list,followerLastKnownDistance):
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
            self.followerLastKnownDistance = MIN_SEPARATION; #By default we asume the leader will move FWD
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
        if(self.mode == 'simulation'):
            print(self.name + ": Actualizamos la maquina de estado del lider")

        else:
            if(self.current_state == EMERGENCY or self.current_state == UNDEFINED): # No puede salir de EMERGENCIA, hay que reiniciar el robot
                self.next_state = EMERGENCY
            #1
            elif(self.current_state == STOP and (self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED or self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = STOP
                print(1)
            #2
            elif(self.current_state == MOVING_FORWARD_MAX and (self.st_information.light_detection == sensors.NO_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = MOVING_FORWARD_MAX
                print(2)
            #3
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and (self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = MOVING_FORWARD_PROPORTIONAL
                print(3)
            #4
            elif(self.current_state == MOVING_FORWARD_MAX and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED):
                self.next_state = MOVING_FORWARD_PROPORTIONAL
                print(4)
            #5
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED):
                self.next_state = MOVING_FORWARD_MAX
                print(5)
            #6
            elif(self.current_state == STOP and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED and self.st_actions.object_picked == False and self.st_actions.grasping == False):
                self.next_state = MOVING_FORWARD_MAX
                print(6)
            #7
            elif(self.current_state == MOVING_FORWARD_MAX and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
                self.st_actions.grasping = True
                print(7)
            #8
            elif(self.current_state == STOP and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED and self.st_actions.object_picked == False and self.st_actions.grasping == False):
                self.next_state = MOVING_FORWARD_PROPORTIONAL
                print(8)
            #9
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
                self.st_actions.grasping = True
                print(9)
            #10
            elif(self.current_state == STOP and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED and self.st_actions.grasping == True):
                self.next_state = PICK_PLACE_OBJECT
                self.st_actions.object_picked = not(self.st_actions.object_picked)
                print(self.st_actions.object_picked)
                print(10)

            #11
            #elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.finished_grasping == False):
            #    self.next_state = PICK_PLACE_OBJECT

            #12
            elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.object_picked == True):
                self.next_state = MOVING_BACKWARD_MAX
                self.st_actions.grasping = False
                print(12)
            #elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.object_picked == True and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED):
            #    self.next_state = MOVING_BACKWARD_MAX
            #    self.st_actions.grasping = False
            #13
            #elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.object_picked == True and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED):
            #    self.next_state = MOVING_BACKWARD_PROPORTIONAL
            #    self.st_actions.grasping = False
            #14
            elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.object_picked == False):
                self.next_state = MOVING_FORWARD_MAX
                self.st_actions.grasping = False
                print(14)
            #elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.object_picked == False and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED):
            #    self.next_state = MOVING_FORWARD_MAX
            #    self.st_actions.grasping = False
            #15
            #elif(self.current_state == PICK_PLACE_OBJECT and self.st_actions.object_picked == False and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED):
            #    self.next_state = MOVING_FORWARD_PROPORTIONAL
            #    self.st_actions.grasping = False
            #16
            elif(self.current_state == MOVING_BACKWARD_MAX and (self.st_information.light_detection == sensors.NO_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = MOVING_BACKWARD_MAX
            #17
            elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL and (self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED or self.st_information.light_detection == sensors.UNKNOWN_LIGHT_DETECTED)):
                self.next_state = MOVING_BACKWARD_PROPORTIONAL
            #18
            elif(self.current_state == MOVING_BACKWARD_MAX and self.st_information.light_detection == sensors.LOW_LIGHT_DETECTED):
                self.next_state = MOVING_BACKWARD_PROPORTIONAL
            #19
            elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL and self.st_information.light_detection == sensors.NO_LIGHT_DETECTED):
                self.next_state = MOVING_BACKWARD_MAX
            #20
            elif(self.current_state == MOVING_BACKWARD_MAX and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
                self.st_actions.grasping = True
            #21
            elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL and self.st_information.light_detection == sensors.HIGH_LIGHT_DETECTED):
                self.next_state = STOP
                self.st_actions.grasping = True

            else:
                self.next_state = UNDEFINED

            self.current_state = self.next_state

    # TODO: Cambiar la maquina de estados cuando esten todos los sensores
    def followerFiniteStateMachine(self):
        """
        Funcion para determinar el siguiente estado del Seguidor

        :param self: Referencia a la instancia desde la clase

        :return: void
        """
        print(self.name + ": Actualizamos la maquina de estados del seguidor")
        if(self.mode == 'simulation'):
            print(self.name + ": Actualizamos la maquina de estado del lider")

        else:
            if(self.current_state == EMERGENCY or self.current_state == UNDEFINED): # No puede salir de EMERGENCIA, hay que reiniciar el robot
                self.next_state = EMERGENCY
            #1
            elif(self.current_state == STOP and (deltaDistance(self) == WAIT)):
                self.next_state = STOP
                print(1)
            #2
            elif(self.current_state == STOP and (deltaDistance(self) == FOLLOW) and self.st_information.ultrasensor_detection > MAX_SEPARATION):
                self.next_state = MOVING_FORWARD_MAX
                print(2)
            #3
            elif(self.current_state == MOVING_FORWARD_MAX and self.st_information.ultrasensor_detection > MAX_SEPARATION ):
                self.next_state = MOVING_FORWARD_MAX
                print(3)
            #4
            elif(self.current_state == MOVING_FORWARD_MAX and self.st_information.ultrasensor_detection < MAX_SEPARATION and self.st_information.ultrasensor_detection > MIN_SEPARATION) :
                self.next_state = MOVING_FORWARD_PROPORTIONAL
                print(4)
            #5
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.ultrasensor_detection < MAX_SEPARATION and self.st_information.ultrasensor_detection > MIN_SEPARATION) :
                self.next_state = MOVING_FORWARD_PROPORTIONAL
                print(5)
            #6
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.ultrasensor_detection < MIN_SEPARATION):
                self.next_state = STOP
                self.followerLastKnownDistance = self.st_information.ultrasensor_detection
                print(6)
            #7
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.ultrasensor_detection > MAX_SEPARATION):
                self.next_state = MOVING_FORWARD_MAX
                print(7)
            #8
            elif(self.current_state == MOVING_FORWARD_MAX and self.st_information.ultrasensor_detection < MIN_SEPARATION):
                self.next_state = STOP
                self.followerLastKnownDistance = self.st_information.ultrasensor_detection
                print(8)
            #9
            elif(self.current_state == MOVING_FORWARD_PROPORTIONAL and self.st_information.ultrasensor_detection < MIN_SEPARATION):
                self.next_state = STOP
                self.followerLastKnownDistance = self.st_information.ultrasensor_detection
                print(9)
            #10
            elif(self.current_state == STOP and (deltaDistance(self) == REPELL) and self.st_information.ultrasensor_detection < MIN_SEPARATION) :
                self.next_state = MOVING_BACKWARD_MAX
                print(10)
            #11
            elif(self.current_state == MOVING_BACKWARD_MAX and self.st_information.ultrasensor_detection < MIN_SEPARATION) :
                self.next_state = MOVING_BACKWARD_MAX
                print(11)
            #12
            elif(self.current_state == MOVING_BACKWARD_MAX and self.st_information.ultrasensor_detection > MIN_SEPARATION and self.st_information.ultrasensor_detection < MAX_SEPARATION) :
                self.next_state = MOVING_BACKWARD_PROPORTIONAL
                print(12)
            #13
            elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL and self.st_information.ultrasensor_detection > MIN_SEPARATION and self.st_information.ultrasensor_detection < MAX_SEPARATION) :
                self.next_state = MOVING_BACKWARD_PROPORTIONAL
                print(13)
            #14
            elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL and self.st_information.ultrasensor_detection > MAX_SEPARATION):
                self.next_state = STOP
                self.followerLastKnownDistance = self.st_information.ultrasensor_detection
                print(14)
            #15
            elif(self.current_state == STOP and (deltaDistance(self) == REPELL) and self.st_information.ultrasensor_detection > MIN_SEPARATION and self.st_information.ultrasensor_detection < MAX_SEPARATION) :
                self.next_state = MOVING_BACKWARD_PROPORTIONAL
                print(15)
            #16
            elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL and self.st_information.ultrasensor_detection < MIN_SEPARATION):
                self.next_state = MOVING_BACKWARD_MAX
                print(16)
            #17
            elif(self.current_state == MOVING_BACKWARD_MAX and  self.st_information.ultrasensor_detection > MAX_SEPARATION):
                self.next_state = STOP
                self.followerLastKnownDistance = self.st_information.ultrasensor_detection

                print(17)
            else:
                self.next_state = UNDEFINED

            self.current_state = self.next_state

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
        if(self.current_state == EMERGENCY or self.current_state == UNDEFINED or STOP):
            controllers.controllerStop(self)

        elif(self.current_state == MOVING_FORWARD_MAX):
            controllers.controllerMovingForwardMax(self)

        elif(self.current_state == MOVING_FORWARD_PROPORTIONAL):
            controllers.controllerMovingForwardProportional(self)

        elif(self.current_state == MOVING_BACKWARD_MAX):
            controllers.controllerMovingBackwardMax(self)

        elif(self.current_state == MOVING_BACKWARD_PROPORTIONAL):
            controllers.controllerMovingBackwardProportional(self)

        elif(self.current_state == PICK_PLACE_OBJECT):
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
            self.error = EXECUTION_SUCCESSFUL

            if(self.current_state == EMERGENCY):
                self.error = EXECUTION_ERROR
            elif(self.current_state == UNDEFINED):
                self.error = EXECUTION_ERROR

            else:
                self.mobile_robot.set_command(self.st_actions.command,int(self.st_actions.movement_motors_pwm))

    # TODO: Añadir la info util y cuando esté todo hecho
    def refreshUserInterface (self):
        """
        Función encargada de refrescar la info para el usuario a intervalos de tiempo correctos

        :param self: Referencia a la instancia desde la clase

        :return void
        """
        if(self.mode == 'simulation'):
            print(self.name + ": Mostramos la informacion util y los errores")

        else:
            print(self.name + ": Estado: " + str(self.current_state))


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
            
            
