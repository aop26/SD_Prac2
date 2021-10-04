#!/usr/bin/python3

import sys
import re

def printUso():
    print("Uso del programa:")
    print("FWQ_Engine [ip:puerto(gestor de colas)] [maximos visitantes] [ip:puerto(gestor de FWQ_WaitingTimeServer)]")
    sys.exit()


if len(sys.argv) != 4:
    print("Número erróneo de argumentos.")
    printUso()

if len(re.split(r'\D', sys.argv[1])) != 5:
    print("Error leyendo ip del lector de colas.")
    printUso()

datosGestor = re.split(':', sys.argv[1])

maxVisitantes = 0
try:
    maxVisitantes = int(sys.argv[2])
except:
    print("El número máximo de visitantes no es un número")
    printUso()

if len(re.split(r'\D', sys.argv[3])) != 5:
    print("Error leyendo ip del lector de colas.")
    printUso()

datosWTS = re.split(':', sys.argv[1])