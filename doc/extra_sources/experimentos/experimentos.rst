*Scripts* de desarrollo propio
==============================
Para probar todas las funcionalidades de los robots hemos creado diversos experimentos con un código de python asociado a cada uno. Por convenio, todos los comentarios y nombres de variables están en inglés. La primera parte y la final de todos los códigos es igual, ya que se trata de conectar y desconectar correctamente con el robot a través de bluetooth. 

Todos los códigos han sido comentados, para entrar en mayor profundidad leer los códigos. Aquí se describen los experimentos llevados a cabo y las dificultades que se han tenido. Además se han probado todos los códigos de ejemplo para poder entender mejor cómo funcionaba cada sensor y actuador, así como las funciones a documentar de aurigapy. Todos los test llevados a cabo deben estar dentro de la carpeta aurigapy para poder ejecutarlos, usar python3 y sudo.


*testingBasicFunctions.py*
--------------------------
En primer lugar hemos querido probar todas las funciones de forma básica para cerciorarnos de que todos los sensores y actuadores funcionan correctamente. Para ello hemos creado el código *testingBasicFunctions.py*. 

El primer test se basa en probar los leds y el altavoz del robot usando un bucle for para ir encendiendo cada led por separado e incrementando el tono del altavoz.

Una vez realizado el primer test, y viendo que los leds funcionan, se activa el array de leds RGB usando un color diferente para cada estado, así tenemos una confirmación visual del estado actual del robot, lo cual es más interactivo que un mensaje en el terminal.

El segundo test prueba los sensores básicos y el estado elegido ha sido verde. Se realiza un bucle for de 20 iteraciones, dando un segundo entre cada iteración, esto nos permite ponerle objetos delante del sensor ultrasonidos, variar la intensidad lumínica de ambos LDR y girar el robot para ver cómo afecta al valor de la brújula y del giroscopio. En cuanto a la temperatura no podemos variar la temperatura de forma drástica, pero el valor no parece alejarse demasiado de la realidad teniendo en cuenta que está dentro de la placa base, donde hará más calor que en la sala.

El tercer test hace la primera prueba de movimiento para ver como funciona, se ha elegido el color azul de estado. Para ello se vuelve a utilizar un ciclo for para ir incrementando el número de grados que se mueve el robot cada vez y la velocidad.

Para el cuarto y último de los test básicos, se combinan las acciones de movimiento con el sensor de ultrasonidos, el estado escogido ha sido el amarillo. En este caso se usa un bucle while que chequeara que la distancia al objeto es menor a 100 (hay que tener en cuenta que este valor no está escalado a ninguna unidad métrica, es directamente el valor analógico que proporciona el sensor). Mientras la distancia no sea menor se moverá hacia adelante por pequeños incrementos de movimiento. Esto se hace así ya que el método *move_to()* es bloqueante, por tanto no podemos leer el sensor mientras se mueve. Una vez se salga del bucle al detectar un obstáculo, hará un pequeño movimiento hacia atrás y girará hacia la izquierda.


*testFollowLight.py*
--------------------
Este experimento se basa en hacer el control de los motores y de los sensores LDR para seguir una fuente de luz. Este problema supone un reto si se usa la función move_to(), debido a que, como hemos explicado antes, es una función bloqueante. En primera instancia usamos dicha función ajustando el valor en grado como la inversa del valor de intensidad lumínica por una constante. Es decir, cuanto más intensa sea la luz menos se moverá, y cuanto más alejada se moverá más. También si detecta un desfase mayor a cierto umbral girará hacia el sensor que tenga un valor mayor. Estas constantes y umbrales han de ser determinadas de forma experimental debido a que la luz ambiente afecta mucho al sensor.

Pero esta primera versión generaba un movimiento muy tosco. Por ello se implementó una versión usando una función similar a *move_to()* pero no bloqueante, esta es *set_command()*. Con ella obtenemos mejores resultados porque el robot no va "ciego", obteniendo una mayor frecuencia del loop, y en todo momento lee el estado de los sensores actuando en consecuencia.


