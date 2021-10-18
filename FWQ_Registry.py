#!/usr/bin/python3

import sys
import customutils as cu

#Lectura y comprobación de argumentos
cu.uso = "FWQ_Registry [Puerto de escucha]"

if len(sys.argv) != 2:
    print("Número erróneo de argumentos.")
    cu.printUso()

puerto = 0
try:
    puerto = int(sys.argv[1])
except:
    print("El puerto no es un número")
    cu.printUso()