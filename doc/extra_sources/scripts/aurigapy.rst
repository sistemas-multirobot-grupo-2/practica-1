Aurigapy
=========

.. highlight:: python

__init__
---------
Se encarga de inicializar las variables necesarias para conectarse y almacenar más tarde información extraída de puertos seriales, el buffer y otras que asisten con el proceso de conexión al robot.

.. py:function:: aurigapy.__init__(self, debug: object = False) -> object

    :param self: El atributo instancia desde el que se ejecuta el método.

    :param object: El objeto.


add_responder
-------------
Añade un nuevo objeto de tipo *responder* al final del vector *responsers*.

.. py:function:: aurigapy.add_responder(self, responder)

    :param responder: Objeto *responder* a añadir.


connect
-------
Establece una conexión con el puerto definido en la variable “port” e informa al usuario haciendo parpadear los LEDs superiores del robot de que la operación ha concluido.

.. py:function:: aurigapy.connect(self, port)

    :param port: Puerto serie al que conectar al objeto.


_process_frame
--------------
Se encarga de comprobar el estado de los *callbacks* recibidos. Si tardan demasiado en responder, se considera que han entrado en *timeout* y terminan la espera, o si se trata de un “blocking” o pausa, espera hasta nueva orden. Si tiene respuesta, comprueba la compatibilidad del *callback* con la marca de tiempo actual, con el tipo de llamada y si existen otros *callbacks* posteriores que manejen el *frame* o entorno.

.. py:function:: aurigapy._process_frame(self, frame)

    :param frame: Estado actual del sistema
    

_data_reader
-------------
Thread que procesa la lectura del puerto serie. Se encarga de detectar paquetes y someterlos al procesado. Leemos el puerto serial para comprobar si existen paquetes. Si los hay, los procesamos y borramos el buffer, verificamos que los *callbacks* no han entrado en *timeout* y si es una llamada a *blocking*. En caso de que no sea ninguno, llamamos a “callback”, notificamos al sistema y “matamos” la conexión.

.. py:function:: aurigapy._data_reader(self)


_write
------
Escribe en el puerto serie. Si se activa la depuración (*debug*), se notifica a través de línea de comandos.

.. py:function:: aurigapy_write(self, data)

    :param data: Mensaje a escribir en el puerto.


reset_robot
-----------
Como indica su nombre, enviamos un nuevo *byte array* para resetear la conexión del robot a través del puerto serie.

.. py:function:: aurigapy.reset_robot(self)


play_sound
-----------
Fuerza al robot a producir un sonido continuo durante cierto tiempo o hasta que se produzca el *callback* especificado.

.. py:function:: aurigapy.play_sound(self, sound=131, duration_ms=1000, callback=None)

    :param sound: Sonido a reproducir. Cuanto más alto sea, más agudo será.

    :param duration_ms: Tiempo durante el que se reproducirá el sonido (en milisegundos).

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_ACK*.


set_led_onboard
---------------
Enciende un LED de la placa con un valor RGB determinado por los parámetros introducidos. Si el LED seleccionado no está en el rango, se lanza un mensaje de error.

.. py:function:: aurigapy.set_led_onboard(self, led, r, g, b, callback=None)

    :param led: Identificador del LED a utilizar.

    :param r: Componente roja de la luz a emitir.

    :param g: Componente verde de la luz a emitir.

    :param b: Componente azul de la luz a emitir.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_ACK*.


set_encoder_motor_rotate_until
------------------------------
Establece la rotación del encoder del motor hasta un ángulo concreto obtenido desde los parámetros introducidos.

.. py:function:: aurigapy.nset_encoder_motor_rotate_until(self, slot, degrees, speed, callback=None)

    :param slot: Puerto de conexión.

    :param degrees: Grados a los que debe girar.

    :param speed: Velocidad.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_ACK*.


set_encoder_motor_rotate
------------------------
Hace que giren los motores deseados del robot a la velocidad definida por los parámetros introducidos.

.. py:function:: aurigapy.set_encoder_motor_rotate(self, slot, speed, callback=None) 

    :param slot: Puerto de conexión.

    :param speed: Velocidad.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_ACK*.


set_command_until
-----------------
Define la dirección del robot entre cuatro candidatos (adelante, atrás, izquierda o derecha) con un cierto ángulo. Función no bloqueante.

.. py:function:: aurigapy.set_command_until(self, command, degrees, speed, callback=None)

    :param command: Dirección en la que ir. Posibles valores: *forward*, *backward*, *left* y *right*.

    :param degrees: Grados a los que debe girar.

    :param speed: Velocidad.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_ACK*.


move_to
-------
Ejecuta el movimiento definido por “set_command_until”.

.. py:function:: aurigapy.move_to(self, command, degrees, speed)

    :param command: Dirección en la que ir. Posibles valores: *forward*, *backward*, *left* y *right*.

    :param degrees: Grados a los que debe girar.

    :param speed: Velocidad.


set_command
-----------
Establece la velocidad positiva o negativa de cada motor en función del comando definido en *set_command_until*. Igual que esta, pero sin tener que pasarle los grados.

.. py:function:: aurigapy.set_command(self, command, speed, callback=None)

    :param command: Dirección en la que ir. Posibles valores: *forward*, *backward*, *left* y *right*.

    :param speed: Velocidad.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_ACK*.


get_encoder_motor_degrees
-------------------------
Obtiene información odométrica de los *encoders* de cada rueda del robot.

.. py:function:: aurigapy.get_encoder_motor_degrees(self, slot: object, callback: object = None) -> object

    :param slot: Puerto de conexión.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_LONG*.

    
get_encoder_motor_speed
-----------------------
Obtiene información de velocidad de los encoders de cada rueda del robot.

.. py:function:: aurigapy.get_encoder_motor_speed(self, slot, callback=None)

    :param slot: Puerto de conexión.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.


get_ultrasonic_reading
----------------------
Obtiene las lecturas del sensor de ultrasonidos incorporado en el robot.

.. py:function:: aurigapy.get_ultrasonic_reading(self, port, callback=None)

    :param port: Puerto de conexión.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.


get_light_sensor
----------------
Extrae la información que proporciona el sensor de luz.

.. py:function:: aurigapy.get_light_sensor(self, port, callback=None)

    :param port: Puerto de conexión.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.


get_light_sensor_onboard
------------------------
Establece y verifica el puerto de conexión del sensor de luz, antes de llamar a su función.

.. py:function:: aurigapy.get_light_sensor_onboard(self, port, callback=None)

    :param port: Puerto de conexión.

    :param callback: Callback del que estar pendiente.


get_sound_sensor
----------------
Obtiene las lecturas del sensor de sonido integrado.

.. py:function:: aurigapy.get_sound_sensor(self, port, callback=None)

    :param port: Puerto de conexión.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.


get_sound_sensor_onboard
------------------------
Establece y verifica el puerto de conexión del sensor de sonido, antes de llamar a su función.

.. py:function:: aurigapy.get_sound_sensor_onboard(self, port, callback=None)

    :param port: Puerto de conexión.

    :param callback: Callback del que estar pendiente.


get_temperature_sensor_onboard
------------------------------
Devuelve las lecturas del sensor de temperatura.

.. py:function:: aurigapy.get_temperature_sensor_onboard(self, port, callback=None)

    :param port: Puerto de conexión.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.


get_line_sensor
---------------
Obtiene las lecturas del sensor infrarrojo dedicado a la función de siguelíneas.

.. py:function:: aurigapy.get_line_sensor(self, port, callback=None)

    :param port: Puerto de conexión.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.


get_compass_sensor
------------------
Recoge las lecturas de la brújula.

.. py:function:: aurigapy.get_compass_sensor(self, port, callback=None)

    :param port: Puerto de conexión.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.


get_gyro_sensor_onboard
-----------------------
Devuelve la información recogida por el giroscopio acerca de la posición del robot en formato de vector de tres componentes (x, y, z).

.. py:function:: aurigapy.get_gyro_sensor_onboard(self, axis, callback=None)

    :param axis: Eje a leer. Opciones: *x*, *y* o *z*.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.


get_pir_sensor
--------------
Devuelve la información recogida por el sensor PIR de presencia.

.. py:function:: aurigapy.get_pir_sensor(self, port, callback=None)

    :param port: Puerto de conexión.

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.


set_servo_grades
----------------
Define y comunica a los servos del motor la posición que deben adoptar, teniendo en cuenta el puerto al que están conectados.

.. py:function:: aurigapy.set_servo_grades(self, port: object, slot: object, degrees: object, callback: object = None) -> object

    :param port: Puerto de conexión

    :param slot: Puerto de conexión

    :param degrees: Grados a girar

    :param callback: Callback del que estar pendiente. En caso de ser *None* (valor por defecto), se atenderá al *Frame.FRAME_TYPE_FLOAT*.

gripper
-------
Activa o desactiva el mecanismo de *gripping* en la pinza del robot.

.. py:function:: aurigapy.gripper(self, command, port, slot)

    :param command: Comando a enviar

    :param port: Puerto de conexión

    :param slot: Puerto de conexión


close
-----
Espera 2 segundos en inactividad antes de terminar el flujo de comandos en el *thread*.

.. py:function:: aurigapy.close(self)


_del_
-----
Termina con la conexión serial.

.. py:function:: aurigapy._del_(self)


