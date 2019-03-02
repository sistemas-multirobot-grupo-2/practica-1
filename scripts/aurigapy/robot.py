#!/usr/bin/env python3


from aurigapy import *
import time


## Constantes y variables globales

# Umbrales de distancia:
FAR_OBJECT_DISTANCE_THRESHOLD_CM   = 40.0 # Cualquier obstáculo a una distancia mayor de la definida aquí se considera que no
                                                       # es un obstáculo, y por lo tanto el vehículo puede continuar recto.

CLOSE_OBJECT_DISTANCE_THRESHOLD_CM = 20.0 # Si la distancia detectada está en el intervalo [CLOSE_OBJECT_DISTANCE_CM, FAR_OBJECT_DISTANCE_CM]
                                                       # el vehículo girará mientras avanza.
                                                       # Cualquier distancia por debajo del unbral CLOSE_OBJECT_DISTANCE_CM, provocará que el 
                                                       # vehículo retroceda mientras gira.
#TODO (YJ): Umbrales de luz
#TODO (YJ): Umbrales de linea (si tiene sentido)
                                                      
# Valores que puede tomar la información extraída a partir de los datos del sensor de ultrasonidos:
NO_OBSTACLE_DETECTED    =  0 # En estos casos, al tratarse de un valor categorial (no númerico) los valores de las etiquetas no son importantes, 
FAR_OBSTACLE_DETECTED   =  1 # basta con que sean diferentes entre sí, para que se puedan distinguir unos de otros!
CLOSE_OBSTACLE_DETECTED =  2
NOT_KNOWN               = -1 # Esta etiqueta la ponemos en negativo para que resulte muy llamativa, se usará en caso de que el sensor de ultrasonidos
                                        # haya dado una lectura errónea.
#TODO (YJ): hacer lo mismo que en ultrasonidos para otros sensores 


#TODO (SJ): Añadir nuevos estados si hiciera falta                                        
# States
STOP                              = 0
MOVING_FORWARD_MAX                = 1
MOVING_FORWARD_PROPORTIONAL       = 2
MOVING_BACKWARD_MAX               = 3
MOVING_BACKWARD_PROPORTIONAL      = 4
PICK_OBJECT                       = 5

#TODO (YJ): Añadir valores estados si hiciera falta
# Valores de los sensores
IMPOSSIBLE_DISTANCE = -1.0
IMPOSIBLE_LUMINESCENSE = -1
LINE_NO_DETECTED = 0
LINE_DETECTED = 1

#TODO (SJ): Añadir nuevos codigos de error si hiciera falta
# Codigos de Error
EXECUTION_ERROR = -1
EXECUTION_SUCCESSFUL = 0

#TODO (SJ): Modificar la clase para que funcione con cualquier robot, definiendo sus propiedades en el constructor 
# Como structs de C
class Config:
    def __init__(self):
        # Valores para la temporización
        #... añadir aquí otros valores de tiempo cuando se añadan nuevos sensores...
        self.ultrasonic_sensor_reading_period_in_millis = 150
        #TODO (YJ): añadiry cambiar el periodo de muestro de los sensores
        self.line_sensor_reading_period_in_millis = 150
        self.light_sensor_reading_period_in_millis = 300
        self.user_interface_refresh_period_in_millis = 500
        
        # Valores para control de motores
        self.max_speed_pwm_value = 100         # hacia adelante
        self.min_real_speed_pwm_value = 20

class Data:
    def __init__(self):
        # ...añadir más campos para guardar datos en caso de añadir nuevos sensores...
        self.detected_distance_in_centimeters = IMPOSSIBLE_DISTANCE
        #TODO (YJ): añadir campos de los sensores
        self.detected_light_in_range = IMPOSIBLE_LUMINESCENSE
        self.detected_right_line = LINE_NO_DETECTED
        self.detected_left_line = LINE_DETECTED

class Information:
    def __init__(self):
        # ...añadir aquí variables para guardar la información extraída por los procesadores
        # a partir de la información de los nuevos sensores que se vayan a instalar.
        self.obstacle_presence = NOT_KNOWN
        #TODO (YJ): añadir informacion de los sensores
        
# Este struct contendrá las salidas que hay que aplicar a cada motor
class Actions:
    def __init__(self):
        self.movement_motors_pwm = 0
        self.command = "forward"
        #TODO (PA):añadir acciones de la herramienta
        self.tool_pwm = 0
        #...añadir otros en caso de añadir motores...
        
# Clase robot
class Robot:
    def __init__(self,bluetooth_path):
        # Definimos el robot y la conexion
        #self.mobile_robot = AurigaPy(debug=False)
        #self.mobile_robot.connect(bluetooth_path)
        
        # Añadimos información de los structs de datos
        self.st_config = Config()
        self.st_meas = Data() # Declaramos un struct de tipo Measurement para guardar las medidas de todos los sensores
        self.st_information = Information()
        self.st_actions = Actions()
        

        # Añadimos información del estado
        self.state = STOP    # Inicializamos esta variable con un valor inicial por defecto para
                             # poder detectar errores en la fase de debug
        self.error = EXECUTION_SUCCESSFUL
        
        # Definimos las variables temporares de refresco
        #TODO (YJ): Añadir nuevas variables para otros sensores
        self.previous_time_ultrasonic = time.time()*1000 # tiempo en millisegundos
        self.previous_time_interface = self.previous_time_ultrasonic
        self.previous_time_line = self.previous_time_ultrasonic
        self.previous_time_light = self.previous_time_ultrasonic
        
        self.current_time_ultrasonic = self.previous_time_ultrasonic
        self.current_time_interface = self.previous_time_ultrasonic
        self.current_time_line = self.previous_time_ultrasonic
        self.current_time_light = self.previous_time_ultrasonic
        
        
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
            
        

