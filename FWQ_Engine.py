#!/usr/bin/python3

import sys
import socket
import customutils as cu


#Lectura y comprobación de argumentos
cu.uso = "FWQ_Engine [ip:puerto(gestor de colas)] [maximos visitantes] [ip:puerto(FWQ_WaitingTimeServer)]"


if len(sys.argv) != 4:
    print("Número erróneo de argumentos.")
    cu.printUso()

addressGestor = cu.checkIP(sys.argv[1],"gestor de colas")

maxVisitantes = 0
try:
    maxVisitantes = int(sys.argv[2])
except:
    print("El número máximo de visitantes no es un número")
    cu.printUso()

addressWTS = cu.checkIP(sys.argv[3],"FWQ_WaitingTimeServer")

#Creación de sockets
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((cu.getIP(),7777))
print("Created server at "+cu.getIP()+" with port "+str(7777))