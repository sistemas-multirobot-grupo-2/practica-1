# Practica 1
Este repositorio que contiene los codigos y la documentación de la primera práctica de la asignatura Sistemas Multirrobot, de 4º curso de Ingeniería Robótica, de la Universidad de Alicante.

# Descripción general de la práctica
En esta práctica hemos redactado la documentación de la librería Aurigapy (desarrollada por Fidel Aznar: https://github.com/fidelaznar/aurigapy) utilizando Sphinx. También hemos implementado un sistema de exploración y navegación colectiva siguiendo una arquitectura jerárquica en Python.

## Material utilizado
Los sistemas utilizados son 2 robots tipo mBot Ranger de Makeblock con las siguientes caracteríticas comunes:
+ Sensor sigue-linea
+ Motores DC que permiten un control diferencial de la dirección del robot
+ Sensor de luz (LDR)
+ Giroscopio
+ Emisor de sonido
+ Sensor de temperatura

Adicionalmente un robot dispone de una pinza y otro de una brújula y un sensor de ultrasonido. Para las **comunicaciontes**, utilizaremos el protocolo de comunicaciones Bluetooth para enlazar un PC con los robots y los robots entre sí.

## *Compilación* de la documentación
Para generar la documentación hemos utilizado **Sphinx**, que es capaz de generar documentación en html y LaTeX (entre otros) a partir de archivos en *reStructuredText*. Para poder leerla, basta con clonar este repositorio con:
```bash
git clone https://github.com/sistemas-multirobot-grupo-2/practica-1
```
Una vez se disponga del repositorio, accederemos al directorio *doc* dentro del mismo, que contiene los archivos de documentación. Para generar tanto la html como la LaTeX, ejecutaremos la instrucción:
```bash
make html latex
```
Una vez ejecutada dicha instrucción, se creará un nuevo directorio llamado *_build*, que contendrá otros llamados *html* y *latex*, que contendrán las documentaciones en sus formatos homónimos. Para ver la *html* debe abrirse el archivo *index.html* con un navegador y, para la *LaTeX*, compilar el archivo *Aurigapy.tex* con la herramienta que se utilice. Por ejemplo, con *pdflatex*, generaríamos el PDF con:
```bash
pdflatex Aurigapy.tex Aurigapy.pdf
```

## Comportamiento general
Colocaremos los robots en fila uno delante de otro en un circuito delimitado por una línea el procedimiento consistirá en utilizar el robot dotado de ultrasonido como director que seguira la línea del circuito y tendrá la responsabilidad de detectar un obstáculo en el camino, detenerse y enviar una orden de detención al robot seguidor. No se retomará la marcha hasta que el robot director no deje de detectar el obstáculo.
