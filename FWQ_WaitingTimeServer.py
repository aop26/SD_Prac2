#!/usr/bin/python3


from os import close
import threading, time
import sys
import re
import socket
import customutils as cu
import atexit
from kafka import KafkaConsumer, consumer

exit = False
dictAtracciones = {}
class kafkaConsumerThread(threading.Thread):
    def __init__(self,ipaddr):
        threading.Thread.__init__(self)
        self.name = "FWQ_WaitingTimeServer kafkaConsumer"
        self.ipaddr = ipaddr
    def run(self):
        global dictAtracciones
        global exit
        sensorReader = KafkaConsumer('sensors',bootstrap_servers=self.ipaddr)
        while not exit:
            msg = next(sensorReader)
            message = str(msg.value).replace('b','').replace("'",'')
            dictAtracciones.update({int(re.split('-',message)[0]):int(re.split('-',message)[1])})
            print(dictAtracciones)
        sensorReader.close()
        

class socketThread(threading.Thread):
    def __init__(self,puerto):
        threading.Thread.__init__(self)
        self.name = "FWQ_WaitingTimeServer server"
        self.puerto = puerto
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((cu.getIP(),puerto))
    def run(self):
        global dictAtracciones
        global exit
        print("Creado servidor en "+cu.getIP()+" con puerto "+str(puerto))
        self.s.listen()
        while not exit:
            (clientSocket, clientIP) = self.s.accept()
            print("Sending current wait times to "+str(clientIP))
            clientSocket.send(str(dictAtracciones).encode('utf-8'))
            clientSocket.close()
        self.s.close()
    def closeConnection(self):
        self.s.close()





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


sensorReaderThread = kafkaConsumerThread(sys.argv[2])
serverThread = socketThread(puerto)

def exit_handler():
    global exit
    exit = True
    print("Cerrando conexión...")
    sensorReaderThread.join()
    serverThread.closeConnection()
    print("Se ha cerrado la conexión con kafka y con Engine")
atexit.register(exit_handler)

sensorReaderThread.start()
serverThread.start()


