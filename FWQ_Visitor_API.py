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
import mapa
import sys
from customutils import *
from os import system
from random import randrange
import socket 
import atexit
import requests

#from prueba import CreaCuenta, IniciaSesion

uso = "FWQ_Visitor [ip:puerto(FWQ_Registry)] [ip:puerto(gestor de colas)] [ip:puerto(engine)]"
HOST = 'localhost'
PORT = 5050
obj = ""
nexit = True
engineCon = -1
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
        asdf = 0
        while(nexit):
            m = getMap(self.addr)
            print(m)
            sleep(1)
    def stop():
        nexit = False
        stopAll()

#Lectura y comprobación de argumentos
uso = "FWQ_Visitor [ip:puerto(FWQ_Registry)] [ip:puerto(gestor de colas)] [ip:puerto(engine)]"

print("se comprueban los args")
if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    printUso()

addrReg = checkIP(sys.argv[1],"FWQ_Registry")

addrGes = checkIP(sys.argv[2],"gestor de colas")

#addrEng = checkIP(sys.argv[3],"engine")


sesionIniciada = False
op = 0
while(op != 6):
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

        if(CreaCuenta(name, password, sys.argv[1])):
            print("Cuenta creada! Ya puedes iniciar sesion.")
        else:
            print("Error creando cuenta")

# =================================================================================================================================================================

    elif(op == 2):
        #INICIAR SESION

        name = input("Escribe tu nombre: ")
        password = HashPassword(input("Escribe tu contraseña: "))
        id = IniciaSesion(name, password, sys.argv[1])
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
                if(ModificaCuenta(id, name, password, sys.argv[1])):
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
            if(EliminaCuenta(id, sys.argv[1])):
                print("Cuenta eliminada.")
                sesionIniciada=False
            else:
                print("Error eliminando cuenta.")

# =================================================================================================================================================================
    
    elif(sesionIniciada and op == 5):

        # ENTRA EN EL PARQUE


        engineCon = kp(sys.argv[2])
        mapConsumer = kafka.KafkaConsumer("engineres",bootstrap_servers=sys.argv[2],group_id=None)#kc(sys.argv[2], 'engineres')
        mapConsumer.poll(timeout_ms=200)
        engineCon.send('movements',EncryptText('join,'+id))
        token = None
        m = -1
        while(not token):
            msg = next(mapConsumer)
            message = DecryptText(msg.value).replace("b'",'').replace("'",'')
            print(message)
            namet=message.split(',')[0]
            if(namet == id):
                token = message.split(',')[1]
                if(token !="NO"):
                    m = strToMap(message.split(',')[2])

        if(m!=-1):
            def exit_handler():
                global nexit
                nexit = False
                engineCon.send('movements',EncryptText('exit,'+token))
                engineCon.close()
                stopAll()
                if(isinstance(obj, socket.socket)):
                    obj.close()

            atexit.register(exit_handler)
            visitor = Visitor(id) # un boejto para un visitor
            m[visitor.x][visitor.y] = visitor

            clientMap = mapa.Mapa(m)

            atracciones = []
            for i in range(20):
                for j in range(20):
                    if(isinstance(clientMap.mapa[i][j], Ride)): # si es una atraccion
                        atracciones.append(m[i][j])

            atraccionSeleccionada = -1
            for i in range(len(atracciones)):
                if(atracciones[i].waitingTime < 60 and atracciones[i].accesible): # si el tiempo de espera es menor a 60
                    atraccionSeleccionada = i
                    print("selecciona:", i)
                    break

            atrVisitadas = []
            timers = []

            hecho = False

            while not hecho:

                if(visitor.wait == 0):
                    atracciones = []
                    for i in range(20):
                        for j in range(20):
                            if(isinstance(m[j][i], Ride)): # si es una atraccion
                                sector = i//10 + j//10*2
                                atracciones.append(m[j][i])
                                if(not (20 <= clientMap.temperaturas[sector][1] <= 30)):
                                    #m[j][i].accesible = False
                                    #clientMap.mapa[j][i].accesible = False
                                    atracciones[len(atracciones)-1].accesible = False
                                else:
                                    #m[j][i].accesible = True
                                    #clientMap.mapa[j][i].accesible = True
                                    atracciones[len(atracciones)-1].accesible = True
                                

                    for i in range(len(timers)):
                        timers[i] -= 1
                    if(len(timers)>0 and timers[0] == 0):
                        atrVisitadas.pop(0)
                        timers.pop(0)


                    if(atraccionSeleccionada == -1 or            # si no hay nada con menos de 60 mins o
                    atracciones[atraccionSeleccionada].waitingTime > 60 or not atracciones[atraccionSeleccionada].accesible): # la atraccion seleccionada tiene mas de 60 mins se vuelve a buscar
                        atraccionSeleccionada = -1
                        for i in range(len(atracciones)):
                            if(atracciones[i].waitingTime < 60 and i not in atrVisitadas and atracciones[i].abierta(mapa.temperaturas)): 
                                atraccionSeleccionada = i
                                print("selecciona:", i, " // " , atracciones[i].x,atracciones[i].y)
                                break


                    if(visitor.timer%60 == 0):
                        if(atraccionSeleccionada == -1): # si no hay nada se mueve random
                            move = [randrange(-1, 2), randrange(-1, 2)]
                            print("random move")
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
                            engineCon.send('movements',EncryptText('move,'+token+','+str(visitor.x)+','+str(visitor.y)+','+str(visitor.id)))
                            mapWhile = True
                            while(mapWhile):
                                msg = next(mapConsumer)
                                message = DecryptText(msg.value).replace("b'",'').replace("'",'')
                                tokent=message.split(',')[0]
                                if(tokent == token):
                                    mr = message.split(',')[1]
                                    mapWhile = False
                                    if(mr !="NO"):
                                        m = strToMap(mr)
                            #print(visitor.x, visitor.y)

                        elif(isinstance(m[visitor.x+move[0]][visitor.y+move[1]], Ride) and visitor.IsIn(atracciones[atraccionSeleccionada])):
                            visitor.wait = 3*60 # espera 3 segundos
                            atrVisitadas.append(atraccionSeleccionada)
                            timers.append(20*60)
                            atraccionSeleccionada = -1
                            print("waiting")

                        elif(isinstance(m[visitor.x+move[0]][visitor.y+move[1]], Ride)):
                            move = [move[0], 0] # si encuentra una atraccion que no es a la que va, la esquiva
                            if(not(isinstance(m[visitor.x+move[0]][visitor.y+move[1]], Visitor))):
                                aux = m[visitor.x][visitor.y]
                                m[visitor.x][visitor.y] = m[visitor.x+move[0]][visitor.y+move[1]]
                                m[visitor.x+move[0]][visitor.y+move[1]] = aux
                                visitor.Move(move)
                                engineCon.send('movements',EncryptText('move,'+token+','+str(visitor.x)+','+str(visitor.y)+','+str(visitor.id)))
                                mapWhile = True
                                while(mapWhile):
                                    msg = next(mapConsumer)
                                    message = DecryptText(msg.value).replace("b'",'').replace("'",'')
                                    tokent=message.split(',')[0]
                                    if(tokent == token):
                                        mr = message.split(',')[1]
                                        mapWhile = False
                                        if(mr !="NO"):
                                            m = strToMap(mr)
                            # else: si es un visitor se espera. 
                        
                        #m = getMap(addrGes,done)
                        if(m==-1):
                            hecho=True
                            break
                        #print(m)

                else:
                    visitor.wait -= 1
                    # espera hasta llegar a 0 y vuelve a buscar una atraccion
                    


                #m = getMap(addrEng,name)
                if(m==-1):
                    hecho=True
                    break
                else:
                    clientMap.Update(m)
                    hecho = clientMap.DrawMapa()

                visitor.timer += 1


            op = 6


    else:
        print("Opcion incorrecta.")
        

