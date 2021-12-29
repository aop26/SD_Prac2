import pygame
from time import sleep
from Ride import *
from Visitor import *
from os import system

from customutils import GetWeather 


NEGRO = (0, 0 ,0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VIOLETA = (98, 0, 255)

TEMP = (200, 200, 200)
CUAD1 = (200, 120, 120)
CUAD2 = (120, 200, 120)
CUAD3 = (120, 120, 200)
CUAD4 = (250, 200, 120)


class Mapa:
    def __init__(self, mapa):
        self.mapa = mapa + []
        self.dimensiones = [1000,1000]
        self.origen = [50, 50]
        self.tamCelda = (self.dimensiones[0] - self.origen[0])/20
        self.temperaturas = GetWeather([])
        pygame.init()
        self.pantalla = pygame.display.set_mode(self.dimensiones) 
        pygame.display.set_caption("Mapa")
        self.hecho = False
        self.reloj = pygame.time.Clock()

        self.fuenteCuad = pygame.font.Font(None, 30) # fuente para los numeros de la cuadricula
        self.fuenteCola = pygame.font.Font(None, 55) # fuente para los numeros de la cola
        self.fuenteTemp = pygame.font.Font(None, 250) # fuente para la temperatura

    def Update(self, newMapa = []):
        if(newMapa != []):
            self.mapa = newMapa + []


    def DrawMapa(self, debug=False):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                pygame.quit()
                return True
            if debug:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_k:
                        for i in range(20):
                            for j in range(20):
                                if(isinstance(self.mapa[i][j], Ride)):
                                    self.mapa[i][j].connected = not self.mapa[i][j].connected 

        self.temperaturas = GetWeather(self.temperaturas)

        self.pantalla.fill(BLANCO)


        # se pintan los colores de los cuadrantes (por casualidad el logo de windows)
        pygame.draw.rect(self.pantalla, CUAD1, [self.origen[0], self.origen[1], 
                                                self.tamCelda*10, self.tamCelda*10])
        pygame.draw.rect(self.pantalla, CUAD2, [self.origen[0]+self.tamCelda*10, self.origen[1],             
                                                self.tamCelda*10, self.tamCelda*10])
        pygame.draw.rect(self.pantalla, CUAD3, [self.origen[0], self.origen[1]+self.tamCelda*10, 
                                                self.tamCelda*10, self.tamCelda*10])
        pygame.draw.rect(self.pantalla, CUAD4, [self.origen[0]+self.tamCelda*10, self.origen[1]+self.tamCelda*10, 
                                                self.tamCelda*10, self.tamCelda*10])


        # se escriben las temperaturas
        if(self.temperaturas[0][0] != "error"):
            txt = self.fuenteTemp.render(str(self.temperaturas[0][1]), True, TEMP)
        else:
            txt = self.fuenteTemp.render("error", True, TEMP)
        self.pantalla.blit(txt, [self.origen[0], self.origen[1]])

        if(self.temperaturas[1][0] != "error"):
            txt = self.fuenteTemp.render(str(self.temperaturas[1][1]), True, TEMP)
        else:
            txt = self.fuenteTemp.render("error", True, TEMP)
        self.pantalla.blit(txt, [self.origen[0]+self.tamCelda*10, self.origen[1]])

        if(self.temperaturas[2][0] != "error"):
            txt = self.fuenteTemp.render(str(self.temperaturas[2][1]), True, TEMP)
        else:
            txt = self.fuenteTemp.render("error", True, TEMP)
        self.pantalla.blit(txt, [self.origen[0], self.origen[1]+self.tamCelda*10])

        if(self.temperaturas[3][0] != "error"):
            txt = self.fuenteTemp.render(str(self.temperaturas[3][1]), True, TEMP)
        else:
            txt = self.fuenteTemp.render("error", True, TEMP)
        self.pantalla.blit(txt, [self.origen[0]+self.tamCelda*10, self.origen[1]+self.tamCelda*10])


        # se dibuja la cuadricula
        for i in range(20):
            pygame.draw.line(self.pantalla, NEGRO, [self.origen[0]+i*self.tamCelda, self.origen[1]], 
                                                   [self.origen[0]+i*self.tamCelda, self.dimensiones[1]], 3)
            pygame.draw.line(self.pantalla, NEGRO, [self.origen[0], self.origen[1]+i*self.tamCelda], 
                                                   [self.dimensiones[0], self.origen[1]+i*self.tamCelda], 3)

    
        # se escriben los numeros de la cuadricula
        pV0 = [self.origen[0]-self.tamCelda*0.6, self.origen[1]+self.tamCelda/2]
        pH0 = [self.origen[0]+self.tamCelda/2, self.origen[1]-self.tamCelda*0.5]

        for i in range(20):
            txt = self.fuenteCuad.render(str(i+1), True, NEGRO)
    
            self.pantalla.blit(txt, [pV0[0], pV0[1] + i*self.tamCelda])
            self.pantalla.blit(txt, [pH0[0] + i*self.tamCelda, pH0[1]])

        

        # se imprimen las cosas del mapa
        for i in range(20):
            for j in range(20):
                if(isinstance(self.mapa[i][j], Ride)):
                    x = i*self.tamCelda + 5
                    y = j*self.tamCelda + 5
                    
                    if(not self.mapa[i][j].connected): # si se desconecta el t de espera es -1
                        txt = self.fuenteCola.render(str(self.mapa[i][j].waitingTime), True, NEGRO) 
                        self.pantalla.blit(txt, [x, y])
                    else:
                        txt = self.fuenteCola.render(str(self.mapa[i][j].waitingTime), True, NEGRO) 
                        self.pantalla.blit(txt, [x, y])
                    
                    sector = i//10 + j//10*2
                    #print(self.temperaturas)
                    if(not (20 <= self.temperaturas[sector][1] <= 30)): # si se desconecta tacha la celda con una X roja
                        x = i*self.tamCelda
                        y = j*self.tamCelda
                        pygame.draw.line(self.pantalla, ROJO, [x+3, y+3], [x+self.tamCelda-1, y+self.tamCelda-1], 5)
                        pygame.draw.line(self.pantalla, ROJO, [x+self.tamCelda-1, y+3], [x+3, y+self.tamCelda-1], 5)

                elif(isinstance(self.mapa[i][j], Visitor)):
                    vI=pygame.image.load(f"./img/{self.mapa[i][j].id}").convert()
                    vI=pygame.transform.scale(vI,[int(self.tamCelda), int(self.tamCelda)])   
                    self.pantalla.blit(vI, [i*self.tamCelda+2, j*self.tamCelda+2])


        pygame.display.flip()
        self.reloj.tick(60)
        return False










if(__name__ == "__main__"):

    v1 = Visitor(1)
    v2 = Visitor(44)
    v3 = Visitor(45)
    v4 = Visitor(16)
    v5 = Visitor(43)


    mapa = [ [0 for j in range(20)] for i in range(20)]
    mapa[0][0] = v1
    mapa[4][3] = v2
    mapa[2][1] = v3
    mapa[4][1] = v4
    mapa[19][19] = v5
    mapa[10][10] = Ride(10, 10, 10)

    
    mapa = Mapa(mapa)
    mapa.temperaturas = GetWeather([])

    hecho = False
    while not hecho:
        hecho = mapa.DrawMapa(True)


    pygame.quit()





