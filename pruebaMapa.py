from mapa import Mapa

# ====================================================================


clientMap = Mapa([ [0 for j in range(20)] for i in range(20)])

hecho = False

while not hecho:
    clientMap.Update()
    hecho = clientMap.DrawMapa()



