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



datosGestor = re.split(':', sys.argv[1])
puertoGestor = 0
if len(re.split(r'\D', sys.argv[1])) != 5 or len(re.split(':', sys.argv[1]))!=2:
    print("Error leyendo ip del gestor de colas.")
    printUso()

try:
    puertoGestor = int(datosGestor[1])
except:
    print("Error leyendo ip del gestor de colas.")
    printUso()

ipGestor = datosGestor[0]

ID= 0
try:
    puerto = int(sys.argv[2])
except:
    print("La ID no es un número")
    printUso()