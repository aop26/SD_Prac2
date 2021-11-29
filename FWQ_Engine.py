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
        visitorAnswerer = cu.kp(self.addr)
        while(nexit):
            global mapaActualizado
            msg = next(visitorReader)
            message = str(msg.value).replace("b'",'').replace("'",'')
            action = message.split('-')[0]
            data = message.split('-')[1]
            #print(data)
            if(action=="join"):
                if((data not in visitantes or visitantes[data]=="NO")  and len(visitantes)>int(sys.argv[2])):
                    visitantes[data]="NO"
                    visitorAnswerer.send('engineres',str(str(data)+'-NO').encode('utf-8'))
                    print(data," no cabe en el parque!")
                    #kafkaProducer = cu.kp(self.addr)
                    #kafkaProducer.send(topic=data+'_map',value="NO".encode('utf-8'))
                    #kafkaProducer.close()
                else:
                    token = uuid4()
                    visitantes[token]=[0,0,time.time()]
                    visitorAnswerer.send('engineres',str(str(data)+','+str(token)+','+cu.mapToStr(mapaActualizado)).encode('utf-8'))
                    print(data," ha iniciado sesión!")
                    #mapaActualizado[0][0]=0#Visitor(int(data.split(',')[2]))
                    ##cu.sendMap(self.addr,mapaActualizado,data)
            elif(action=="move" and data.split(',')[3] in visitantes and visitantes[data.split(',')[3]]!="NO"):
                token = data.split(',')[3]
                mapaActualizado[visitantes[token][0]][visitantes[token][1]]=0
                posx=int(data.split(',')[0])
                posy=int(data.split(',')[1])
                visitantes[token] = [posx,posy]
                mapaActualizado[posx][posy]=Visitor(int(data.split(',')[2]))
                ##cu.sendMap(self.addr,mapaActualizado,name)
            elif(action=="exit"):
                mapaActualizado[visitantes[data][0]][visitantes[data][1]]=0
                visitantes.pop(data)
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
                print("Cannot connect to waiting time server: ",e)
            time.sleep(2)
    def stop(self):
        print("Stopping server connection")
        cu.stopAll()
        nexit = False
        quit()

'''class MapThread(threading.Thread):
    def __init__(self,puerto):
        threading.Thread.__init__(self)
        self.name = "FWQ_WaitingTimeServer server"
        self.puerto = puerto
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((cu.getIP(),puerto))
    def run(self):
        global mapaActualizado
        global exit
        global visitantes
        print("Creado servidor en "+cu.getIP()+" con puerto "+str(puerto))
        self.s.listen()
        while True:
            #print("Esperando")
            (clientSocket, clientIP) = self.s.accept()
            #print("Sending current map to "+str(clientIP))
            name = clientSocket.recv(4096).decode('utf-8')
            sleep(0.5)
            if(name in visitantes and visitantes[name]!="NO"):
                clientSocket.send(cu.mapToStr(mapaActualizado).encode('utf-8'))
            else:
                print(name, "where do you think you are going?")
                print(visitantes)
                clientSocket.send("NO".encode('utf-8'))
            clientSocket.close()
        self.s.close()
    def closeConnection(self):
        self.s.close()'''


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

# puerto = 0
# try:
#     puerto = int(sys.argv[4])
# except:
#     print("El puerto no es un número")
#     cu.printUso()


waitTime = WaitingTimeThread(addressWTS)
visitorMove = VisitorMovementThread(sys.argv[1])
#mapSender = MapThread(puerto)

def exit_handler():
    print("stopping")
    global nexit
    nexit = False
    cu.stopAll()
    waitTime.stop()
    #visitorMove.stop()
    # cerrar cosas
atexit.register(exit_handler)

waitTime.start()
visitorMove.start()
#mapSender.start()

hecho = False
print("Iniciados threads del servidor de tiempos de espera y del consumidor kafka")
while not hecho:
    hecho = mapaEngine.DrawMapa()

quit()
