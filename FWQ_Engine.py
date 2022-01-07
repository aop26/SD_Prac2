#!/usr/bin/python3

from re import split
import sys
import socket
import customutils as cu
import threading
import time
import atexit
from mapa import *
from Ride import *
from Visitor import *
from uuid import uuid4
global mapaEngine
nexit = True
mapaEngine = Mapa(cu.mapaVacio())
mapaActualizado = cu.mapaVacio()
visitantes = {}

class VisitorMovementThread(threading.Thread):
    def __init__(self, addr):
        threading.Thread.__init__(self)
        self.addr = addr
        self.name = "FWQ_EngineVisitorConsumer"
    def run(self):
        global nexit
        global visitantes
        visitorReader = cu.kc(self.addr,'movements')
        visitorReader.poll(timeout_ms=200)
        visitorAnswerer = cu.kp(self.addr)
        while(nexit):
            global mapaActualizado
            msg = next(visitorReader)
            message = cu.DecryptText(msg.value).replace("b'",'').replace("'",'')
            action = message.split(',')[0]
            data = message.split(',')[1]
            if(action=="join"):
                if((data not in visitantes or visitantes[data]=="NO")  and len(visitantes)>int(sys.argv[2])):
                    visitantes[data]="NO"
                    txt = cu.EncryptText(str(str(data)+',NO'))
                    visitorAnswerer.send('engineres',txt)
                    print(data," no cabe en el parque!")
                else:
                    token = uuid4()
                    visitantes[str(token)]=[0,0,time.time()]
                    txt = cu.EncryptText(str(str(data)+','+str(token)+','+cu.mapToStr(mapaActualizado)))#cu.EncryptText(str(str(data)+','+str(token)+','+cu.mapToStr(mapaActualizado)))
                    visitorAnswerer.send('engineres',txt)
                    print(data," ha iniciado sesión!")
            elif(action=="move" and data in visitantes and visitantes[data]!="NO"):
                mapaActualizado[visitantes[data][0]][visitantes[data][1]]=0
                posx=int(message.split(',')[2])
                posy=int(message.split(',')[3])
                visitantes[data] = [posx,posy, time.time()]
                mapaActualizado[posx][posy]=Visitor(int(message.split(',')[4]))
                visitorAnswerer.send('engineres',cu.EncryptText(str(str(token)+','+cu.mapToStr(mapaActualizado))))
            elif(action=="exit"and data in visitantes and visitantes[data]!="NO"):
                mapaActualizado[visitantes[data][0]][visitantes[data][1]]=0
                visitantes.pop(data)
            mapaEngine.Update(mapaActualizado)
    def stop():
        cu.stopAll()


class WaitingTimeThread(threading.Thread):
    def __init__(self, addr):
        threading.Thread.__init__(self)
        self.addr = addr
        self.name = "FWQ_EngineWaitingServerConsumer"

    def run(self):
        global nexit
        while(nexit):
            global mapaActualizado
            # comprueba el server de tiempos
            s = socket.socket()
            try:
                s.connect((self.addr[0],int(self.addr[1])))
                res = s.recv(4096).decode('utf-8')
                #print("Recibidos datos del servidor de tiempos de espera en ",self.addr)
                res = res.replace('{','').replace('}','').split(', ')
                for i in res:
                    id = int(i.split(":")[0])
                    waitTime = int(i.split(":")[1])
                    pos, wtc, mp = cu.leerAtr(id)
                    ride = Ride(pos[0],pos[1],waitTime)
                    ride.connected=False
                    mapaActualizado[pos[0]][pos[1]]= ride
                mapaEngine.Update(mapaActualizado)
            except Exception as e:
                print("No se puede conectar al waiting time server: ",e)
            time.sleep(2)
    def stop(self):
        print("Conexion con waiting time server detenida")
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
atexit.register(exit_handler)

waitTime.start()
visitorMove.start()

hecho = False
print("Iniciados threads del servidor de tiempos de espera y del consumidor kafka")
while not hecho:
    hecho = mapaEngine.DrawMapa()
    f = open("map.txt","w")
    f.write(cu.mapToStr(mapaActualizado))
    f.close()
    delT = []
    for t in visitantes:
        if(visitantes[t]!="NO" and time.time()-visitantes[t][2]>1):
            visitorAnswerer = cu.kp(sys.argv[1])
            visitorAnswerer.send('engineres',cu.EncryptText(str(str(t)+','+cu.mapToStr(mapaActualizado))))
            visitorAnswerer.close()
        elif(visitantes[t]!="NO" and time.time()-visitantes[t][2]>5):
            delT.append(t)

            
    for token in delT:
        print(token,"disconnected")
        mapaActualizado[visitantes[token][0]][visitantes[token][1]]=0
        visitantes.pop(token)
        mapaEngine.Update(mapaActualizado)

quit()
