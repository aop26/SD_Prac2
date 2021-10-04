#!/usr/bin/python3

import sys
import re

def printUso():
    print("Uso del programa:")
    print("FWQ_WaitingTimeServer [Puerto de escucha] [ip:puerto(gestor de colas)]")
    sys.exit()


if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    printUso()

puerto= 0
try:
    puerto = int(sys.argv[1])
except:
    print("El puerto no es un número")
    printUso()

datosGestor = re.split(':', sys.argv[2])
puertoGestor = 0
if len(re.split(r'\D', sys.argv[2])) != 5 or len(re.split(':', sys.argv[2]))!=2:
    print("Error leyendo ip del gestor de colas.")
    printUso()

try:
    puertoGestor = int(datosGestor[1])
except:
    print("Error leyendo ip del gestor de colas.")
    printUso()

ipGestor = datosGestor[0]