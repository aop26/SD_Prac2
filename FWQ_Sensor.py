#!/usr/bin/python3

import sys
import re

def printUso():
    print("Uso del programa:")
    print("FWQ_Sensor [ip:puerto(gestor de colas)] [ID atracción]")
    sys.exit()


if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    printUso()



if len(re.split(r'\D', sys.argv[1])) != 5:
    print("Error leyendo ip del gestor de colas.")
    printUso()

datosGestor = re.split(':', sys.argv[1])

ID= 0
try:
    puerto = int(sys.argv[2])
except:
    print("La ID no es un número")
    printUso()