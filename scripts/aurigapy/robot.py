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
        self.mobile_robot = AurigaPy(debug=False)
        self.mobile_robot.connect(bluetooth_path)
        
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
        #self.detected_distance_in_centimeters = IMPOSSIBLE_DISTANCE # Inicializamos con un valor imposible, de esta forma
                                                               # si hay cualquier problema con el sensor nos daremos cuenta
                                                               # al leer la información de depurado.
          
        self.current_time_ultrasonic = time.time()*1000 # Consultamos el tiempo en milisegundos
        
        # y comprobamos si se ha cumplido el tiempo mínimo para consultar el sensor
        if ( self.current_time_ultrasonic - self.previous_time_ultrasonic > self.st_config.ultrasonic_sensor_reading_period_in_millis ):
            # en caso de que sea momento de leer el sensor actualizamos la medida anterior
            self.st_meas.detected_distance_in_centimeters = self.mobile_robot.get_ultrasonic_reading(10)


            # y actualizamos el contador con el valor de tiempo en el que se ha realizado la última lectura del sensor.
            self.previous_time_ultrasonic = time.time()*1000
       
        #else:
            # en caso contrario en realidad no tenemos que hacer nada, simplemente devolveremos el 
            # valor que tenga la variable, que será el de la última lectura válida, o la IMPOSSIBLE_DISTANCE,
            # en caso de que todavía no se haya producido ninguna medida.
                                                                  
    # ...aquí habría que añadir las funciones para leer cada uno de los demás sensores que instalemos...
    # TODO (YJ): def readLineSensor(self)
    # TODO (YJ): def readLightSensor(self) 
    
    
    # Función genérica que debe ir llamando a cada una de las funciones específicas para rellenar el struct de "Data" con 
    # los datos de todos los sensores instalados.
    def readSensors(self):
        
        # Llamamos a la función que lee el sensor de ultrasonidos
        self.readUltraSensor()
        # TODO (YJ): añadir las demas funciones de sensores

        # Si tuvieramos más sensores, habría que añadir las funciones para leerlos y guardar los
        # datos en otros campos del struct "st_meas"
  
    # Procesador específico para extaer información acerca de la presencia de obstáculos en base a los datos del 
    # sensor de ultrasonidos.
    def processUltrasonicSensorData(self):
        self.st_information.obstacle_presence = NOT_KNOWN

        if ( self.st_meas.detected_distance_in_centimeters == IMPOSSIBLE_DISTANCE ):
            self.st_information.obstacle_presence = NOT_KNOWN # En caso de que no dispongamos de lecturas válidas del sensor no podemos extraer
                                       # información, esto (como se verá más adelante) hará que el vehículo se detenga.

        else:
            if ( self.st_meas.detected_distance_in_centimeters > FAR_OBJECT_DISTANCE_THRESHOLD_CM ): # Si el obstáculo más proximo está por encima del
                                                                      # umbral, consideramos que tenemos vía libre.
                self.st_information.obstacle_presence = NO_OBSTACLE_DETECTED 
            
            else:
                if ( self.st_meas.detected_distance_in_centimeters > CLOSE_OBJECT_DISTANCE_THRESHOLD_CM ): # En caso contrario, si la distancia es mayor que
                                                                           # la mínima permitida para seguir avanzando, consideramos
                                                                           # que se trata de un obstáculo lejano.                                                                          
                    self.st_information.obstacle_presence = FAR_OBSTACLE_DETECTED
                else:
                    self.st_information.obstacle_presence = CLOSE_OBSTACLE_DETECTED # En caso contrario el obstáculo está en la zona cercana.
           
    # ...aquí habría que añadir las funciones para procesar cada uno de los demás sensores que instalemos...
    # TODO (YJ): def processLineSensor(self)
    # TODO (YJ): def processLightSensor(self) 
    
    # Función para extraer la información a partir de los datos 'en crudo'.
    def processData(self):
        self.processUltrasonicSensorData()
        
        # TODO (YJ): añadir las demas funciones de sensores
        # ...Aquí habría que añadir las distintas llamadas a los procesadores específicos para los datos de 
        # cada sensor

    # Función para determinar qué tarea se va a llevar a cabo a partir de la información extraída a partir
    # de los datos de los sensores.
    def updateFiniteStateMachine(self):
        
        if self.st_information.obstacle_presence == NOT_KNOWN:
            self.state = STOP    # Si hay error en el sensor pararemos motores.
        
        elif self.st_information.obstacle_presence == NO_OBSTACLE_DETECTED: 
            self.state = MOVING_FORWARD_MAX # En caso de que se detecte un obstáculo lejano, continuaremos
                                            # la marcha hacia adelante usando un controlador proporcional
                                            # con la distancia (más detalles en las implementaciones 
                                            # de los controladores específicos).
        elif self.st_information.obstacle_presence == FAR_OBSTACLE_DETECTED:
            self.state = MOVING_FORWARD_PROPORTIONAL # En caso de que se detecte un obstáculo lejano, continuaremos
                                                   # la marcha hacia adelante usando un controlador proporcional
                                                   # con la distancia (más detalles en las implementaciones 
                                                   # de los controladores específicos).
                                                       
        elif self.st_information.obstacle_presence == CLOSE_OBSTACLE_DETECTED:
            self.state = MOVING_LEFT_MAX # Si el obstáculo se encuentra en la zona cercana se hará
                                                         # retroceder al vehículo mientras gira. También implementaremos
                                                         # un control proporcional a la distancia, como se verá en la sección
                                                         # de controladores específicos.
        #TODO (SJ): Añadir nuevos casos en la maquina de estados
        else:
            self.state = STOP # En caso de que venga algún valor extraño pararíamos el vehículo.

    # Controlador específico para parar motores
    def controllerStop(self):
        # Símplemente pondremos ambos motores a cero. Por este motivo no necesitamos que la función
        self.st_actions.movement_motors_pwm = 0
        self.st_actions.command = "forward"
    
    #TODO (PA): Cambiar los controladores para seguir la linea, no chocar, etc
    # Controlador específico que se utiliza para avanzar a la máxima velocidad permitida por configuración
    def controllerMovingForwardMax(self):
        # Al usar este controlador avanzaremos empleando la máxima velocidad permitida por la
        # configuración
        self.st_actions.movement_motors_pwm = self.st_config.max_speed_pwm_value
        self.st_actions.command = "forward"

    # Controlador específico para ir mas lento.
    def controllerForwardProportional(self):
        # En este caso vamos a emplear la distancia medida por el ultrasonidos
        # para ajustar la velocidad del vehículo.
        # y lo que haremos será reducir
        # la velocidad del motor en función de la distancia al obstáculo.
        #
        # Sabemos que este controlador se va a usar cuando los obstáculos estén a una
        # distancia en el intervalo [CLOSE_OBJECT_DISTANCE_CM, FAR_OBJECT_DISTANCE_CM]
        # por lo que escalaremos la velocidad del motor
        # para que quede en el intervalo [0, max_speed_pwm_value]

        # como el PWM tiene que ser un número entero, primero hacemos un casting a flotante "(float)max_speed_pwm_value"
        pwm = self.st_config.min_real_speed_pwm_value + (float(self.st_config.max_speed_pwm_value - self.st_config.min_real_speed_pwm_value) * (self.st_meas.detected_distance_in_centimeters - CLOSE_OBJECT_DISTANCE_THRESHOLD_CM) / (FAR_OBJECT_DISTANCE_THRESHOLD_CM - CLOSE_OBJECT_DISTANCE_THRESHOLD_CM))

        # y luego redondeamos y pasamos a tipo int
        self.st_actions.movement_motors_pwm = int(round(pwm))
        
        self.st_actions.command = "forward"

    # ... Aquí habrá que añadir otros controladores específicos, como por ejemplo un siguelíneas, o uno para poner el vehículo perpendicular a una pared... #
    # TODO (PA): def controllerBackwardMax(self)
    # TODO (PA): def controllerBackwardProportional(self)
    # TODO (PA): def openTool(self)
    # TODO (PA): def closeTool(self)

    # Función genérica que llama al controlador específico adecuado en función de la tarea
    # que se deba realizar. 
    def controller(self):
        if self.state == STOP:
            self.controllerStop()
        elif self.state == MOVING_FORWARD_MAX:
            self.controllerMovingForwardMax()     
        elif self.state == MOVING_FORWARD_PROPORTIONAL:
            self.controllerForwardProportional()         
             
        #... si hubiesen otros controladores habría que llamarlos desde otros casos...# 
        #TODO (SJ): Modificar y añadir los estados y controladores
        else:
            # En el caso de que nos llegase un valor extraño en la variable current_state
            # utilizaremos el controlador del estado inicial (que símplemente mantiene
            # parado el vehículo).
            self.st_actions = self.controllerStop()  

    # Función encargada de pasar a motores los comandos calculados por los controladores
    # este es el último punto antes de actuar sobre los motores,por lo que tenemos que 
    # ser cuidadosos de no enviar valores indeseados... En este caso la máquina es pequeña
    # pero imaginemos que vamos a acelerar un coche o un camión... hay que pensar bien
    # antes de actuar!!
    def execute(self):
        # Usaremos un código de error para detectar posibles anomalías en los controladores
        self.error = EXECUTION_SUCCESSFUL

        #if ( self.st_actions.movement_motors_pwm > self.st_config.max_speed_pwm_value or self.st_actions.movement_motors_pwm < 0 ):
            # En caso de que el valor esté fuera de rango activaremos el código de error
        #    self.error = EXECUTION_ERROR 
        
        # En caso de que no concuerde la  activaremos el código de error
        if ( self.state == MOVING_FORWARD_MAX and self.st_actions.command is not "forward" ):
            self.error = EXECUTION_ERROR
        if ( self.state == MOVING_FORWARD_PROPORTIONAL and self.st_actions.command is not "forward" ):
            self.error = EXECUTION_ERROR
        if ( self.state == MOVING_LEFT_MAX and self.st_actions.command is not "left" ):
            self.error = EXECUTION_ERROR
        #...si añadimos mas estados hay que añadir nuevos casos...#    
        
        if( self.error == EXECUTION_ERROR ): 
            # En caso de error paramos motores por seguridad.
            self.st_actions.movement_motors_pwm = 0
        
        #TODO (SJ): Modificar y añadir los estados y controladores

        # Finalmente aplicamos a motor los PWM calculados.
        self.mobile_robot.set_command(command=self.st_actions.command, speed=self.st_actions.movement_motors_pwm)

    # Función encargada de refrescar la info para el usuario a intervalos de tiempo correctos
    def refreshUserInterface (self):
        # Procedemos con la parte de sincronización, esta funciona igual que la que hemos empleado antes en la función readUltraSensor, 
        # (en esa función están todos los detalles comentados, por lo que ahora no los repetiremos)
        self.current_time_interface = time.time()*1000 # Consultamos el tiempo en milisegundos

        # y comprobamos si se ha cumplido el tiempo mínimo para publicar los datos por el puerto serie
        if ( self.current_time_interface - self.previous_time_interface > self.st_config.user_interface_refresh_period_in_millis ):
            # en caso de que sea momento de refrescar la info, pasamos a escribir en el puerto serie:
            print("Distance reading = " + str(self.st_meas.detected_distance_in_centimeters))

            print("State = " + str(self.state))

            #print("Left motor pwm = ")
            #println(st_actions.left_motor_pwm)

            #print("Right motor pwm = ")
            #println(st_actions.right_motor_pwm) 

            print("Error code = " + str(self.error))
            
            print("Speed = " + str(self.st_actions.movement_motors_pwm))
            print("Command = " + str(self.st_actions.command))
            
            #TODO(SJ): Modificar y añadir los estados y controladores
            
            # y actualizamos el contador con el valor de tiempo en el que se ha realizado la última lectura del sensor.
            self.previous_time_interface = time.time()*1000

    
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
            
        

