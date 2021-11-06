from mapa import Mapa
from Visitor import *
from Ride import  *
from random import randrange
# ====================================================================


v = Visitor(23) # un boejto para un visitor

m = [ [0 for j in range(20)] for i in range(20)] # se solicita el mapa a engine, de moemento es un array vacio
m[10][7] = Ride(10, 7, 45)
m[15][2] = Ride(15, 2, 45)
m[v.x][v.y] = v

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
    if(v.wait == 0):
        if(atraccionSeleccionada == -1 or            # si no hay nada con menos de 60 mins o
        atracciones[atraccionSeleccionada].waitingTime > 60): # la atraccion seleccionada tiene mas de 60 mins se vuelve a buscar
            atraccionSeleccionada = -1
            for i in range(len(atracciones)):
                if(atracciones[i].waitingTime < 60 and i not in atrVisitadas): 
                    atraccionSeleccionada = i
                    print("selecciona:", i)
                    break


        if(v.timer%60 == 0):
            if(atraccionSeleccionada == -1): # si no hay nada se mueve random
                move = [randrange(-1, 2), randrange(-1, 2)]
                print("random", end="")
            else:
                dX = atracciones[atraccionSeleccionada].x - v.x
                dY = atracciones[atraccionSeleccionada].y - v.y
                move = [ int(dX/abs(dX)) if dX!=0 else 0, 
                         int(dY/abs(dY)) if dY!=0 else 0]

            if(not(0<v.x+move[0]<20)):
                move[0] = 0
            if(not(0<v.y+move[1]<20)):
                move[1] = 0


            if(not(isinstance(m[v.x+move[0]][v.y+move[1]], Ride) or isinstance(m[v.x+move[0]][v.y+move[1]], Visitor))):
                aux = m[v.x][v.y]
                m[v.x][v.y] = m[v.x+move[0]][v.y+move[1]]
                m[v.x+move[0]][v.y+move[1]] = aux
                v.Move(move)
                print(v.x, v.y)
            elif(isinstance(m[v.x+move[0]][v.y+move[1]], Ride) and v.IsIn(atracciones[atraccionSeleccionada])):
                v.wait = 3*60 # espera 3 segundos
                atrVisitadas.append(atraccionSeleccionada)
                atraccionSeleccionada = -1
                print("waiting")
            elif(isinstance(m[v.x+move[0]][v.y+move[1]], Ride)):
                move = [move[0], 0] # si encuentra una atraccion que no es a la que va, la esquiva
                if(not(isinstance(m[v.x+move[0]][v.y+move[1]], Visitor))):
                    aux = m[v.x][v.y]
                    m[v.x][v.y] = m[v.x+move[0]][v.y+move[1]]
                    m[v.x+move[0]][v.y+move[1]] = aux
                    v.Move(move)
                # else: si es un visitor se espera. 

    else:
        v.wait -= 1
        # espera hasta llegar a 0 y vuelve a buscar una atraccion
        


    clientMap.Update()
    hecho = clientMap.DrawMapa()

    v.timer += 1

    



