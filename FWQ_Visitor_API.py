#!/usr/bin/python3

import re
from selectors import PollSelector
import threading
import time
from kafka.consumer import group
from kafka.consumer.group import KafkaConsumer
from kafka.errors import KafkaConfigurationError
from kafka.producer.kafka import KafkaProducer
from kafka.structs import TopicPartition
from FWQ_Registry import FORMAT
from Visitor import *
from Ride import *
from mapa import *
import sys
from customutils import *
from os import system
from random import randrange
import socket 
import atexit
import requests

from prueba import CreaCuenta, IniciaSesion


HOST = 'localhost'
PORT = 5050
obj = ""
nexit = True
def exit_handler():
    global nexit
    global engineCon
    nexit = False
    stopAll()
    if(isinstance(obj, socket.socket)):
        obj.close()
    if(isinstance(engineCon, KafkaConsumer)):
        engineCon.close()

atexit.register(exit_handler)
m = "NO"
class MapUpdateThread(threading.Thread):
    def __init__(self, addr):
        threading.Thread.__init__(self)
        self.addr = addr
        self.name = "FWQ_EngineVisitorMapConsumer"
        self.visitantes = 0
    def run(self):
        global nexit
        global m
        mapConsumer = None
        #while not mapConsumer:
        #    try:
        #        topic = name+"_map"
        #        mapConsumer= KafkaConsumer(bootstrap_servers=self.addr,group_id=None,auto_offset_reset="earliest")#KafkaConsumer(bootstrap_servers=sys.argv[2],group_id=None)#
        #        mapConsumer.assign([TopicPartition(topic,0)])
        #        #mapConsumer.assign([TopicPartition(name+'_map',0)])
        #        #mapConsumer.poll()
        #        #mapConsumer.seek_to_beginning()
        #    except Exception as e:
        #        print("No se ha podido conectar a kafka. Reintentando en 1 segundo.\n",e)
        #        time.sleep(1)
        #        if(not nexit):
        #            quit()
        #print("waiting")
        asdf = 0
        while(nexit):
            m = getMap(self.addr)
            print(m)
            sleep(1)
            #print("waiting",asdf)
            #asdf+=1
            #print(mapConsumer.highwater(TopicPartition(topic,0)))
            #msg = next(mapConsumer)
            #message = str(msg.value).replace('b','').replace("'",'')
            #m=False
            #if(message == "NO"):
            #    m= "NO"
            #else:
            #    m= cu.strToMap(message)
            #mapConsumer.close()
            #mapConsumer= KafkaConsumer(bootstrap_servers=self.addr,group_id=None,auto_offset_reset="latest")#KafkaConsumer(bootstrap_servers=sys.argv[2],group_id=None)#
            #mapConsumer.assign([TopicPartition(topic,0)])
    def stop():
        nexit = False
        stopAll()

#Lectura y comprobación de argumentos
uso = "FWQ_Visitor [ip:puerto(FWQ_Registry)] [ip:puerto(gestor de colas)] [ip:puerto(engine)]"

print("se comprueban los args")
if len(sys.argv) != 4:
    print("Número erróneo de argumentos.")
    printUso()

addrReg = checkIP(sys.argv[1],"FWQ_Registry")

addrGes = checkIP(sys.argv[2],"gestor de colas")

addrEng = checkIP(sys.argv[3],"engine")


sesionIniciada = False
op = 0
while(op != 4):
    obj = ""
    print("1. Crear cuenta.")
    print("2. Iniciar sesion")
    if(sesionIniciada):
        print("3. Editar cuenta.")
        print("4. Eliminar cuenta")
        print("5. Entrar en parque.")

    op = int(input("Elige una opcion: "))


    if(op == 1):
        # CREAR CUENTA
        
        name = input("Escribe tu nombre: ")
        password = HashPassword(input("Escribe tu contraseña: "))

        if(CreaCuenta(name, password)):
            print("Cuenta creada! Ya puedes iniciar sesion.")
        else:
            print("Error creando cuenta")

# =================================================================================================================================================================

    elif(op == 2):
        #INICIAR SESION

        name = input("Escribe tu nombre: ")
        password = HashPassword(input("Escribe tu contraseña: "))
        id = IniciaSesion(name, password)
        if(id != -1):
            print("Sesion iniciada!")
            sesionIniciada = True
        else:
            print("Error iniciando sesion.")
            sesionIniciada = False

# =================================================================================================================================================================
 
    elif(sesionIniciada and op == 3):
        # EDITAR CUENTA

        while(True):
            print("Que campo quieres editar?")
            print("nombre[n], contraseña[c], guardar[g], cancelar[q]")

            editOp = input("Elige una opcion: ")
   
            if(editOp == "n"):
                name = input("Escribe tu nombre: ")
            elif(editOp == "c"):
                password = HashPassword(input("Escribe tu contraseña: "))
            elif(editOp == "g"):
                if(ModificaCuenta(id, name, password)):
                    print("Cuenta modificada!")
                else:
                    print("Error modifcando la cuenta.")
                break

            elif(editOp == "q"):
                break
            else:
                print("Opcion incorrecta.")

# =================================================================================================================================================================
 
    elif(sesionIniciada and op == 4):
        # ELIMINAR CUENTA

        sn = input("Estas seguro de que quieres eliminar tu cuenta?[s/n]")

        if(sn == "s" or sn == "S"):
            if(EliminaCuenta(id)):
                print("Cuenta eliminada.")
            else:
                print("Error eliminando cuenta.")

# =================================================================================================================================================================
    
    elif(sesionIniciada and op == 5):

        # ENTRA EN EL PARQUE



        #engineCon = cu.kp(sys.argv[2])
        #print(respuesta)
        #engineCon.send('movements',('join-'+done).encode('utf-8'))
        #updateMapThread = MapUpdateThread(addrEng)
        #updateMapThread.start()
        #m = False
        #while(m == False):
        #    print("Waiting for engine")
        #    sleep(1)
        #m = cu.getMap(sys.argv[2],name)
        m=-1
        while(m==-1):
            m = cu.getMap(addrEng,done)
        if(m!=-1):
            def exit_handler():
                global nexit
                nexit = False
                engineCon.send('movements',('exit-'+done).encode('utf-8'))
                engineCon.close()
                cu.stopAll()
                if(isinstance(obj, socket.socket)):
                    obj.close()

            atexit.register(exit_handler)
            visitor = Visitor(done) # un boejto para un visitor

            #m = [ [0 for j in range(20)] for i in range(20)] # se solicita el mapa a engine, de moemento es un array vacio
            m[visitor.x][visitor.y] = visitor

            clientMap = Mapa(m)

            atracciones = []
            for i in range(20):
                for j in range(20):
                    if(isinstance(m[i][j], Ride)): # si es una atraccion
                        atracciones.append(m[i][j])

            atraccionSeleccionada = -1
            for i in range(len(atracciones)):
                if(isinstance(m[i][j], Ride) and atracciones[i].waitingTime < 60): # si el tiempo de espera es menor a 60
                    atraccionSeleccionada = i
                    print("selecciona:", i)
                    break

            atrVisitadas = []

            hecho = False

            while not hecho:

                if(visitor.wait == 0):
                    atracciones = []
                    for i in range(20):
                        for j in range(20):
                            if(isinstance(m[j][i], Ride)): # si es una atraccion
                                atracciones.append(m[j][i])

                    if(atraccionSeleccionada == -1 or            # si no hay nada con menos de 60 mins o
                    atracciones[atraccionSeleccionada].waitingTime > 60): # la atraccion seleccionada tiene mas de 60 mins se vuelve a buscar
                        atraccionSeleccionada = -1
                        for i in range(len(atracciones)):
                            if(atracciones[i].waitingTime < 60 and i not in atrVisitadas): 
                                atraccionSeleccionada = i
                                print("selecciona:", i,atracciones[i].x,atracciones[i].y)
                                break


                    if(visitor.timer%60 == 0):
                        if(atraccionSeleccionada == -1): # si no hay nada se mueve random
                            move = [randrange(-1, 2), randrange(-1, 2)]
                            print("random", end="")
                        else:
                            dX = atracciones[atraccionSeleccionada].x - visitor.x
                            dY = atracciones[atraccionSeleccionada].y - visitor.y
                            move = [ int(dX/abs(dX)) if dX!=0 else 0, 
                                    int(dY/abs(dY)) if dY!=0 else 0]

                        if(not(0<visitor.x+move[0]<20)):
                            move[0] = 0
                        if(not(0<visitor.y+move[1]<20)):
                            move[1] = 0


                        if(not(isinstance(m[visitor.x+move[0]][visitor.y+move[1]], Ride) or isinstance(m[visitor.x+move[0]][visitor.y+move[1]], Visitor))):
                            aux = m[visitor.x][visitor.y]
                            m[visitor.x][visitor.y] = m[visitor.x+move[0]][visitor.y+move[1]]
                            m[visitor.x+move[0]][visitor.y+move[1]] = aux
                            visitor.Move(move)
                            engineCon.send('movements',('move-'+str(visitor.x)+','+str(visitor.y)+','+str(visitor.id)+','+done).encode('utf-8'))
                            print(visitor.x, visitor.y)

                        elif(isinstance(m[visitor.x+move[0]][visitor.y+move[1]], Ride) and visitor.IsIn(atracciones[atraccionSeleccionada])):
                            visitor.wait = 3*60 # espera 3 segundos
                            atrVisitadas.append(atraccionSeleccionada)
                            atraccionSeleccionada = -1
                            print("waiting")

                        elif(isinstance(m[visitor.x+move[0]][visitor.y+move[1]], Ride)):
                            move = [move[0], 0] # si encuentra una atraccion que no es a la que va, la esquiva
                            if(not(isinstance(m[visitor.x+move[0]][visitor.y+move[1]], Visitor))):
                                aux = m[visitor.x][visitor.y]
                                m[visitor.x][visitor.y] = m[visitor.x+move[0]][visitor.y+move[1]]
                                m[visitor.x+move[0]][visitor.y+move[1]] = aux
                                visitor.Move(move)
                                engineCon.send('movements',('move-'+str(visitor.x)+','+str(visitor.y)+','+str(visitor.id)+','+done).encode('utf-8'))
                            # else: si es un visitor se espera. 
                        
                        m = cu.getMap(addrEng,done)
                        if(m==-1):
                            hecho=True
                            break
                        #print(m)

                else:
                    visitor.wait -= 1
                    # espera hasta llegar a 0 y vuelve a buscar una atraccion
                    


                #m = cu.getMap(addrEng,name)
                if(m==-1):
                    hecho=True
                    break
                else:
                    clientMap.Update(m)
                    hecho = clientMap.DrawMapa()

                visitor.timer += 1


            op = 4


    else:
        print("Opcion incorrecta.")
        

