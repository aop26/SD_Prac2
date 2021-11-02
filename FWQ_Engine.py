#!/usr/bin/python3

import sys
import socket
import customutils as cu
import threading
import time
import atexit
from mapa import *
from Ride import *
from Visitor import *

global mapaEngine
nexit = True
mapaEngine = Mapa(cu.mapaVacio())
mapaActualizado = cu.mapaVacio()

class VisitorMovementThread(threading.Thread):
    def __init__(self, addr):
        threading.Thread.__init__(self)
        self.addr = addr
        self.name = "FWQ_EngineVisitorConsumer"
        self.visitantes = {}
    def run(self):
        global nexit
        visitorReader = cu.kc(self.addr,'visitors')
        while(nexit):
            global mapaActualizado
            msg = next(visitorReader)
            #mapaActualizado = cu.mapaVacio()
            # recibe movimientos y repsonde enviando el mapa
            mapaEngine.Update(mapaActualizado)
    def stop():
        cu.stopAll()


class WaitingTimeThread(threading.Thread):
    def __init__(self, addr):
        threading.Thread.__init__(self)
        self.addr = addr
        self.name = "FWQ_EngineWaitingServerConsumer"

    def run(self):
        print("prueba")
        global nexit
        while(nexit):
            global mapaActualizado
            # comprueba el server de tiempos
            s = socket.socket()
            try:
                s.connect((self.addr[0],int(self.addr[1])))
                res = s.recv(4096).decode('utf-8')
                print("Recibidos datos del servidor de tiempos de espera en ",self.addr)
                res = res.replace('{','').replace('}','').split(', ')
                for i in res:
                    id = int(i.split(":")[0])
                    waitTime = int(i.split(":")[1])
                    pos, wtc, mp = cu.leerAtr(id)
                    ride = Ride(pos[0],pos[1],waitTime)
                    mapaActualizado[pos[0]][pos[1]]= ride
                mapaEngine.Update(mapaActualizado)
            except Exception as e:
                print("Cannot connect to waiting time server: ",e)
            time.sleep(2)
    def stop(self):
        print("Stopping server connection")
        cu.stopAll()
        nexit = False
        quit()



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




waitTime = WaitingTimeThread(addressWTS)
visitorMove = VisitorMovementThread(sys.argv[1])

def exit_handler():
    print("stopping")
    global nexit
    nexit = False
    cu.stopAll()
    waitTime.stop()
    visitorMove.stop()
    # cerrar cosas
atexit.register(exit_handler)

waitTime.start()
visitorMove.start()

hecho = False
print("Iniciados threads del servidor de tiempos de espera y del consumidor kafka")
while not hecho:
    hecho = mapaEngine.DrawMapa()

quit()