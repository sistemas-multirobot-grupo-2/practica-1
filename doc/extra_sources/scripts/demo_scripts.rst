*Scripts* de ejemplo
====================
A lo largo de esta sección describimos el comportamiento que implementan cada uno de los *scripts* de ejemplo proporcionados junto a la librería *aurigapy*.

*compass.py*
------------
Lee la información de fecha y hora del ordenador así como de la brújula del robot. Esa información es mostrada por la terminal del ordenador.

*frame.py*
----------
Herramienta de conversión de datos en crudo a datos interpretables y de datos interpretados a datos en crudo.

*giro.py*
---------
La función devuelve la fecha y hora actual y las orientaciones en los ejes X, Y, Z en grados.

*leds.py*
---------
Elige un led al azar en el rango de 1 a 11 y un código rgb en el rango de 0 a 10 la información del led a encender y el código rgb es lo que define el color del led elegido aleatoriamente que se va a encender, este proceso se repite 400 veces.

*light.py*
----------
Muestra por terminal información de la fecha y hora e información de la intensidad lumínica percibida, empíricamente hemos obtenido valores mínimos de 7 y máximos de 999 por lo que suponemos que el rango se encuentra entre 0 y 1024.

*line.py*
---------
Muestra la fecha y hora y valores enteros en el rango de 0 a 3 siguiendo la siguiente lógica:

* 0: Ambos sensores de línea detectan línea.
* 1: El sensor izquierdo detecta línea pero el derecho no.
* 2: El sensor derecho detecta línea pero el izquierdo no.
* 3: Ningún sensor detecta línea.

*move_to.py*
------------
Muestra la fecha y hora y hace una prueba de movimiento de las ruedas suponiendo que se trata de un sistema diferencial, primero mueve el robot hacia delante y luego lo gira sobre si mismo hacia la derecha.

*play_sound_multiple.py*
------------------------
Se conecta a dos robots y les hace reproducir 10 sonidos, cada uno más agudo que el anterior. También cambia el color del anillo de LEDs, dándoles valores iguales a todos los canales pero cada vez más altos (10 iteraciones).

*play_sound.py*
---------------
Se conecta a un robot y le hace reproducir sonidos cada vez más agudos. Cada uno de los pitidos dura 100 ms.

*sound.py*
----------
Se conecta y lee los datos captados por el sensor de sonido. Luego los imprime por pantalla junto al *timestamp* en el que fueron captados.

*temperature.py*
----------------
Obtiene la temperatura percibida por el sensor y la muestra por pantalla junto al *timestamp* correspondiente a la lectura.

*ultrasonic.py*
---------------
Muestra por pantalla las lecturas del sensor de ultrasonido al lado del *timestamp* pertinente a cada una.

