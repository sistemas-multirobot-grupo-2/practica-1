Introducción
============

Introducción
------------
Los sistemas multirrobot están frecuentemente conformados por robots de bajas capacidades que colaboran de alguna forma para lograr resolver tareas más rápido o que son demasiado complejas para ser resueltas sólo por uno de ellos.

En nuestro caso, utilizaremos kits de Makeblock, orientados a la educación, pero buenas opciones para implementar aplicaciones donde varios robots interactúen, ya que se ajustan relativamente bien al concepto de *sistema multirrobot* expuesto.

Consideramos preciso indicar que para el desarrollo de esta práctica vamos a programar los robots en Python. Desarrollaremos los códigos en nuestros ordenadores y se los cargaremos a través de Bluetooth.


*Setup*
-------
Dada la necesaria interactuación inalámbrica a través de Bluetooth, es necesario establecer conexión entre nuestros equipos y los robots. Con este propósito, investigamos cómo hacerlo de la forma más conveniente posible. En el laboratorio somos varios grupos, cada uno con sus robots, por lo que el procedimiento *tradicional* de conexión utilizando la GUI complicaba y ralentizaba todo, ya que detectábamos los robots de otros grupos y todos tenían como identificador *Makeblock*. Por esto, optamos por establecer las conexiones basándonos en las direcciones MAC.

Con este propósito, comenzamos escaneándo los dispositivos Bluetooth cercanos con: 

.. code-block:: bash

   $ hcitool scan

Una vez localizada la MAC de nuestro robot (cosa que hicimos escaneando, apagando el robot y volviendo a escanear para ver cuál dejaba de detectarse), pasamos a realizar la conexión. Este proceso difiere según qué versión de Ubuntu se esté utilizando. 

Ubuntu 14.04
~~~~~~~~~~~~
En caso de estar utilizando Ubuntu 14.04, es posible editar un fichero de configuración (*rfcomm.conf*), que permite dejar permanentemente definidas las MAC de los robots y facilitar su conexión posterior, tal y como explicamos a continuación (fuente: https://askubuntu.com/questions/248817/how-to-i-connect-a-raw-serial-terminal-to-a-bluetooth-connection).

Pasamos a configurar el puerto en el archivo */etc/bluetooth/rfcomm.conf* escribiendo (hemos probado y pueden conectarse 2 robots a distintos puertos por un mismo canal):

.. code-block:: javascript

   [puerto] ("rfcomm0", "rfcomm1"...)
   {
     bind no;
     device [MAC_del_chip_Bluetooth];
     channel 1;
     comment "Serial Port";
   }

De este modo, para cada dispositivo a configurar pasaríamos a tener algo como:

.. code-block:: javascript

   rfcomm1
   {
     bind no;
     device 00:1B:10:31:39:CB;
     channel 1;
     comment "Serial Port";
   }

Por último, en Ubuntu 14, nos conectamos al puerto configurado utilizando la instrucción:

.. code-block:: bash

   $ sudo rfcomm connect [numero_puerto ("0" para conectar con "rfcomm0", "1" para "rfcomm1"...)]

Un ejemplo, en caso de querer conectarse al dispositivo configurado en rfcomm1:

.. code-block:: bash

   $ sudo rfcomm connect 1 

Ubuntu 16.04
~~~~~~~~~~~~
En caso de estar utilizando Ubuntu 16.04, la instrucción a ejecutar para conectarnos sería:

.. code-block:: bash

   $ sudo rfcomm connect <dev (puerto rfcomm)> <MAC> [canal]

Por ejemplo:

.. code-block:: bash

   $ sudo rfcomm connect 1 00:1B:10:31:39:CB 1 #Conectarse al robot 1 desde /dev/rfcomm1
   $ sudo rfcomm connect 8 00:0D:19:03:5F:18 1 #Conectarse al robot 8 desde /dev/rfcomm8
