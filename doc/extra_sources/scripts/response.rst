Response
========

__init__
--------
Inicializa un objeto *response*, asignándole todos los parámetros que *__init__* recibe como argumentos.

.. py:function:: response.__init__(self, timestamp, timeout, response_type, response_callback, response_event=None)

   :param self: Una referencia a la instancia actual de la clase, desde la que se está llamando al método. En este caso, la instancia que se está creando.
   :param timestamp: Marca temporal o registro de tiempo. Sirve para indicar cuándo se generó la instancia.
   :param timeout: *Timeout* o tiempo máximo de ejecución asignado a la instancia.
   :param response_type: Tipo de respuesta de la instancia.
   :param response_callback: Callback asociada a la instancia.
   :param response_event: Evento asociado a la instancia.


generate_response_async
-----------------------
.. py:function:: response.generate_response_async(callback, response_type, timeout=0.3)

   :param callback: Función con 2 parámetros (valor_respuesta, timeout). *Timeout* es *true* si se ha llamado por *timeout* y no por respuesta.
   :param response_type: El tipo de respuesta a generar.
   :param timeout: El *timeout* a asignar a la respuesta. Por defecto valdrá 0.3.
   :return: Respuesta asíncrona con el tiempo actual como *timestamp*, sin *response_event* y con los *timeout*, *response_type* y *callback* especificados.


generate_response_block
-----------------------
.. py:function:: response.generate_response_block(response_type, timeout=0.3)

   :param response_type: El tipo de respuesta a generar.
   :param timeout: El *timeout* a asignar a la respuesta. Por defecto valdrá 0.3.
   :return: Respuesta con el tiempo actual como *timestamp*, sin *callback*, con *threading.Event()* como *response_event* y con los *timeout* y *response_type* especificados.


is_timeout
----------
Comprueba si se ha alcanzado el *timeout* especificado.

.. py:function:: response.is_timeout(self)

   :return: *True* en caso de que la suma del *timestamp* y del *timeout* sea menor que el tiempo actual. *False* en cualquier otro caso.


wait_blocking
-------------
Esperar a que suceda el evento asignado a la respuesta. Si no hay ninguno, se dará un error.

.. py:function:: response.wait_blocking(self)

