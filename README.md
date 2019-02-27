# Practica 1
Repositorio que contiene los codigos y documentación de la primera práctica

# Descripción general de la práctica
En esta práctica hemos implementado un sistema de comportamientos colectivos de tipo exploración y navegación colectiva siguiendo una arquitectura jerárquica en python.

## Material utilizado
Los sistemas utilizados son 2 robots tipo mBot Ranger de Makeblock con las siguientes caracteríticas comunes:
+ Sensor sigue-linea
+ Motores DC que permiten un control diferencial de la dirección del robot
+ Sensor de luz (LDR)
+ Giroscopio
+ Emisor de sonido
+ Sensor de teperatura

Adicionalmente un robot dispone de una pinza y otro de una brújula y un sensor de ultrasonido

## Comunicaciones
Utilizaremos el protocolo de comunicaciones bluetooth para comunicar un PC con los robots y los robots entre sí.

## Comportamiento general
Colocaremos los robots en fila uno delante de otro en un circuito delimitado por una línea el procedimiento consistirá en utilizar el robot dotado de ultrasonido como director que seguira la línea del circuito y tendrá la responsabilidad de detectar un obstáculo en el camino, detenerse y enviar una orden de detención al robot seguidor. No se retomará la marcha hasta que el robot director no deje de detectar el obstáculo.
