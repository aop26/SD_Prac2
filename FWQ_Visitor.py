#!/usr/bin/python3

import sys
import customutils as cu
from os import system

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

    elif(op == 2):

        while(True):

            # hay que ver como inicia sesion.
            
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
                if(data[1] is not None):
                    # envia contraseña
                # se desconecta de registry
            elif(editOp == "q"):
                break
            else:
                print("Opcion incorrecta.")

        system("clear")

    elif(op == 3):
        clientMap = Mapa([ [0 for j in range(20)] for i in range(20)])

        hecho = False

        while not hecho:
            clientMap.Update()
            hecho = clientMap.DrawMapa()

        op = 4


