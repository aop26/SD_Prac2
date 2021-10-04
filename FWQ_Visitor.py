#!/usr/bin/python3

import sys
import customutils as cu

#Lectura y comprobación de argumentos
cu.uso = "FWQ_Visitor [ip:puerto(FWQ_Registry)] [ip:puerto(gestor de colas)]"


if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    cu.printUso()

addrReg = cu.checkIP(sys.argv[1],"FWQ_Registry")

addrGes = cu.checkIP(sys.argv[2],"gestor de colas")