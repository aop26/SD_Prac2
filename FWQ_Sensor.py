#!/usr/bin/python3

import sys
import customutils as cu

#Lectura y comprobación de argumentos
cu.uso = "FWQ_Sensor [ip:puerto(gestor de colas)] [ID atracción]"


if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    cu.printUso()


addressGestor = cu.checkIP(sys.argv[1],"gestor de colas")

ID= 0
try:
    puerto = int(sys.argv[2])
except:
    print("La ID no es un número")
    cu.printUso()