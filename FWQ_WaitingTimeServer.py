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
    print("La ID no es un número")
    printUso()

if len(re.split(r'\D', sys.argv[2])) != 5:
    print("Error leyendo ip del gestor de colas.")
    printUso()

datosGestor = re.split(':', sys.argv[2])

