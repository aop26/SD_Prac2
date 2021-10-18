#!/usr/bin/python3

from Visitor import *
from Ride import *
from mapa import *
import sys
import customutils as cu
from os import system
from random import randrange

#Lectura y comprobación de argumentos
cu.uso = "FWQ_Visitor [ip:puerto(FWQ_Registry)] [ip:puerto(gestor de colas)]"


if len(sys.argv) != 3:
    print("Número erróneo de argumentos.")
    cu.printUso()

addrReg = cu.checkIP(sys.argv[1],"FWQ_Registry")

addrGes = cu.checkIP(sys.argv[2],"gestor de colas")


while(op != 4):
    print("1. Crear perfil.")
    print("2. Editar perfil.")
    print("3. Entrar en parque.")
    op = int(input("Elige una opcion."))


    if(op == 1):
        # se conecta a registry

        alias = input()
        # se envia alias

        name = input()
        # se envia name

        password = input()
        # se envia password
        # se desconecta de registry
        system("clear")

# =================================================================================================================================================================
 
    elif(op == 2):

        # hay que ver como iniciar sesion.
        sesionIniciada = False


        while(sesionIniciada):
            
            print("Que campo quieres editar?")
            print("nombre[n], contraseña[c], guardar[g], cancelar[q]")

            editOp = input("Elige una opcion: ")
            data = [None, None]

            if(editOp == "n"):
                data[0] = input()
            elif(editOp == "c"):
                data[1] = input()
            elif(editOp == "g"):
                # se conecta a registry
                if(data[0] is not None):
                    # envia nombre
                    txt = data[0]
                if(data[1] is not None):
                    # envia contraseña
                    txt = data[1]
                # se desconecta de registry
            elif(editOp == "q"):
                break
            else:
                print("Opcion incorrecta.")

        system("clear")

# =================================================================================================================================================================
    
    elif(op == 3):
        # se inicia sesion
        visitor = Visitor() # un boejto para un visitor

        m = [ [0 for j in range(20)] for i in range(20)] # se solicita el mapa a engine, de moemento es un array vacio
        
        clientMap = Mapa(m)

        atracciones = []
        for i in range(20):
            for j in range(20):
                if(m[i][j]): # si es una atraccion
                    atracciones.append(m[i][j])

        atraccionSeleccionada = -1
        for i in range(len(atracciones)):
            if(atracciones[i] < 60): # si el tiempo de espera es menor a 60
                atraccionSeleccionada = i



        hecho = False

        while not hecho:

            if(atraccionSeleccionada == -1 or            # si no hay nada con menos de 60 mins o
               atracciones[atraccionSeleccionada] > 60): # la atraccion seleccionada tiene mas de 60 mins se vuelve a buscar
                atraccionSeleccionada = -1
                for i in range(len(atracciones)):
                    if(atracciones[i] < 60): 
                        atraccionSeleccionada = i


            if(visitor.timer == 60):
                if(atraccionSeleccionada == -1): # si no hay nada se mueve random
                    move = [randrange(-1, 1), randrange(-1, 1)]
                else:
                    dX = atracciones[atraccionSeleccionada].x - visitor.x
                    dY = atracciones[atraccionSeleccionada].y - visitor.y
                    move = [ dX/abs(dX), dY/abs(dY)]
                visitor.Move(move)
                    


            clientMap.Update()
            hecho = clientMap.DrawMapa()

            visitor.timer += 1


        op = 4

    else:
        print("Opcion incorrecta.")
        




