#!/usr/bin/python3

import sys
import re
import ipaddress;

def printUso():
    print("Uso del programa:")
    print("FWQ_Engine [ip:puerto(gestor de colas)] [maximos visitantes] [ip:puerto(FWQ_WaitingTimeServer)]")
    sys.exit()


if len(sys.argv) != 4:
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

maxVisitantes = 0
try:
    maxVisitantes = int(sys.argv[2])
except:
    print("El número máximo de visitantes no es un número")
    printUso()

datosWTS = re.split(':', sys.argv[3])
if len(re.split(r'\D', sys.argv[3])) != 5 or len(re.split(':', sys.argv[3]))!=2:
    print("Error leyendo ip de FWQ_WaitingTimeServer.")
    printUso()

try:
    puertoWTS = int(datosWTS[1])
except:
    print("Error leyendo ip de FWQ_WaitingTimeServer.")
    printUso()

ipWTS = datosWTS[0]