#!/usr/bin/python3

import sys
import re

def printUso():
    print("Uso del programa:")
    print("FWQ_Registry [Puerto de escucha]")
    sys.exit()

if len(sys.argv) != 2:
    print("Número erróneo de argumentos.")
    printUso()

puerto = 0
try:
    puerto = int(sys.argv[1])
except:
    print("El puerto no es un número")
    printUso()