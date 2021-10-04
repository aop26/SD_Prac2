#!/usr/bin/python3

import sys
import socket
import customutils as cu
import atexit
from kafka import KafkaConsumer

#Lectura y comprobación de argumentos
cu.uso = "FWQ_WaitingTimeServer [Puerto de escucha] [ip:puerto(gestor de colas)]"


if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    cu.printUso()

puerto= 0
try:
    puerto = int(sys.argv[1])
except:
    print("El puerto no es un número")
    cu.printUso()

addrGes = cu.checkIP(sys.argv[2],"gestor de colas")

#Creación de sockets
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((cu.getIP(),puerto))
print("Created server at "+cu.getIP()+" with port "+str(puerto))
atexit.register(lambda : s.close())
sensorReader = KafkaConsumer('sensors',bootstrap_servers=sys.argv[2])
while True:
    