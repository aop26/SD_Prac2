#!/usr/bin/python3

import sys
import re

def printUso():
    print("Uso del programa:")
    print("FWQ_Visitor [ip:puerto(FWQ_Registry)] [ip:puerto(gestor de colas)]")
    sys.exit()


if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    printUso()



if len(re.split(r'\D', sys.argv[1])) != 5:
    print("Error leyendo ip de FWQ_Registry.")
    printUso()

datosRegistry = re.split(':', sys.argv[1])

if len(re.split(r'\D', sys.argv[2])) != 5:
    print("Error leyendo ip del lector de colas.")
    printUso()

datosGestor = re.split(':', sys.argv[2])