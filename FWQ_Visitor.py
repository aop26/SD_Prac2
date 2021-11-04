#!/usr/bin/python3

from FWQ_Registry import FORMAT
from Visitor import *
from Ride import *
from mapa import *
import sys
import customutils as cu
from os import system
from random import randrange
import socket 
import atexit

HOST = 'localhost'
PORT = 5050
obj = ""
def exit_handler():
    global nexit
    nexit = False
    cu.stopAll()
    if(isinstance(obj, socket.socket)):
        obj.close()

atexit.register(exit_handler)



#Lectura y comprobación de argumentos
cu.uso = "FWQ_Visitor [ip:puerto(FWQ_Registry)] [ip:puerto(gestor de colas)]"

print("se comprueban los args")
if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    cu.printUso()

addrReg = cu.checkIP(sys.argv[1],"FWQ_Registry")

addrGes = cu.checkIP(sys.argv[2],"gestor de colas")

op = 0
while(op != 4):
    obj = ""
    print("1. Crear perfil.")
    print("2. Editar perfil.")
    print("3. Entrar en parque.")
    op = int(input("Elige una opcion: "))


    if(op == 1):
        # se conecta a registry

        obj = socket.socket()
        #print(addrReg)
        obj.connect((addrReg[0], addrReg[1]))
        obj.send("c".encode('utf-8'))

        done = False
        while(not done):
            name = input("Escribe tu nombre: ")
            password = input("Escribe tu contraseña: ")
            txt = name + "//" + password
            obj.send(txt.encode('utf-8'))
            #system("clear")

            respuesta, done = obj.recv(4096).decode(FORMAT).split("//")
            print(respuesta)

            if(done == "1"):
                done = True
                obj.send("FIN".encode('utf-8'))
                obj.close()
        


# =================================================================================================================================================================
 
    elif(op == 2):

        # hay que ver como iniciar sesion.
        sesionIniciada = False
        obj = socket.socket()
        obj.connect((addrReg[0], addrReg[1]))
        obj.send("l".encode('utf-8'))

        name = input("Escribe tu nombre: ")
        password = input("Escribe tu contraseña: ")
        txt = name + "//" + password
        obj.send(txt.encode('utf-8'))

        #system("clear")

        respuesta, done = obj.recv(4096).decode(FORMAT).split("//")
        print(respuesta)
        if(done != "-1"):
            sesionIniciada = True

        obj.send("m".encode("utf-8"))

        while(sesionIniciada):
            
            print("Que campo quieres editar?")
            print("nombre[n], contraseña[c], guardar[g], cancelar[q]")

            editOp = input("Elige una opcion: ")
            data = ["BLANK", "BLANK"]

            if(editOp == "n"):
                name = input("Escribe tu nombre: ")
            elif(editOp == "c"):
                password = input("Escribe tu contraseña: ")
            elif(editOp == "g"):
                txt = name + "//" + password
                obj.send(txt.encode('utf-8'))
                #system("clear")

                respuesta, done = obj.recv(4096).decode(FORMAT).split("//")
                print(respuesta)
                obj.send("FIN".encode('utf-8'))
                obj.close()
                break

            elif(editOp == "q"):
                break
            else:
                print("Opcion incorrecta.")


# =================================================================================================================================================================
    
    elif(op == 3):

        sesionIniciada = False
        obj = socket.socket()
        obj.connect((addrReg[0], addrReg[1]))
        obj.send("l".encode('utf-8'))

        name = input("Escribe tu nombre: ")
        password = input("Escribe tu contraseña: ")
        txt = name + "//" + password
        obj.send(txt.encode('utf-8'))
        
        #system("clear")

        respuesta, done = obj.recv(4096).decode(FORMAT).split("//")
        print(respuesta)
        if(done != "-1"):
            sesionIniciada = True
        obj.send("FIN".encode('utf-8'))
        obj.close()
        
        if(sesionIniciada):
            visitor = Visitor(done) # un boejto para un visitor

            m = [ [0 for j in range(20)] for i in range(20)] # se solicita el mapa a engine, de moemento es un array vacio
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
                    if(atraccionSeleccionada == -1 or            # si no hay nada con menos de 60 mins o
                    atracciones[atraccionSeleccionada].waitingTime > 60): # la atraccion seleccionada tiene mas de 60 mins se vuelve a buscar
                        atraccionSeleccionada = -1
                        for i in range(len(atracciones)):
                            if(atracciones[i].waitingTime < 60 and i not in atrVisitadas): 
                                atraccionSeleccionada = i
                                print("selecciona:", i)
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
                            # else: si es un visitor se espera. 

                else:
                    visitor.wait -= 1
                    # espera hasta llegar a 0 y vuelve a buscar una atraccion
                    


                clientMap.Update()
                hecho = clientMap.DrawMapa()

                visitor.timer += 1


            op = 4


    else:
        print("Opcion incorrecta.")
        









