Serialcom
=========

__init__
--------
.. py:function:: serialcom.__init__(self)

   :param self: Referencia a la instancia desde la que se llama al método. En este caso, la instancia que se está construyendo.
   :return: Instancia *serialcom* vacía, sin ningún puerto (variable *_serial*) asignado.


connect
-------
Asigna un puerto al objeto.

.. py:function:: serialcom.connect(self, port='/dev/tty.Makeblock-ELETSPP')

   :param port: Puerto a asignarle a la instancia desde la que se llama al método.


device
------
.. py:function:: serialcom.device(self)

   :return: El puerto asignado a la instancia desde la que se llama al método.


scan_serial_ports
-----------------
Crea una lista con todos los posibles puertos serie (teniendo en cuenta si se está en un sistema Windows, GNU/Linux o Darwin, advirtiendo si la plataforma actual no es una de las mencionadas). Crea un objeto *serial* para cada uno e intenta conectarse para luego cerrarlo. Si no ha habido ningún fallo, lo añade a la lista que se devuelve.

.. py:function:: serialcom.scan_serial_ports()

   :return: Lista con los puertos a los que es posible conectarse.


write
-----
Escribe los datos solicitados en el puerto serie del objeto desde el que se está llamando al método.

.. py:function:: serialcom.write(self, data)

   :param data: Datos a escribir en el puerto serie.


read
----
.. py:function:: serialcom.read(self)

   :return: Lectura del puerto serie asignado al objeto desde el que se está llamado al método.


is_open
-------
Comprueba si el puerto que corresponde a la instancia está abierto. Utiliza *isOpen()*.

.. py:function:: serialcom.is_open(self)

   :return: *True* si el puerto está abiero y *false* en cualquier otro caso.


in_waiting
----------
Devuelve el número de *bytes* en el *buffer* de entrada. Utiliza *inWaiting()*.

.. py:function:: serialcom.in_waiting(self)

   :return: Número de *bytes* en el *buffer* de entrada. 


close
-----
Cierra el puerto serie, liberándolo y dejándolo disponible para otros procesos.

.. py:function:: serialcom.close(self)
