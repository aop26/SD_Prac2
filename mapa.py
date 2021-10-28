import pygame
from time import sleep
from Ride import *
from Visitor import *

NEGRO = (0, 0 ,0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VIOLETA = (98, 0, 255)

CUAD1 = (200, 120, 120)
CUAD2 = (120, 200, 120)
CUAD3 = (120, 120, 200)
CUAD4 = (200, 200, 120)


class Mapa:
    def __init__(self, mapa):
        self.mapa = mapa + []
        self.dimensiones = [1000,1000]
        self.origen = [50, 50]
        self.tamCelda = (self.dimensiones[0] - self.origen[0])/20

        pygame.init()
        self.pantalla = pygame.display.set_mode(self.dimensiones) 
        pygame.display.set_caption("Mapa")
        self.hecho = False
        self.reloj = pygame.time.Clock()

        self.fuenteCuad = pygame.font.Font(None, 30) # fuente para los numeros de la cuadricula
        self.fuenteCola = pygame.font.Font(None, 55) # fuente para los numeros de la cola


    def Update(self, newMapa = []):
        if(newMapa != []):
            self.mapa = newMapa + []


    def DrawMapa(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                pygame.quit()
                return True

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
                    txt = self.fuenteCola.render(str(self.mapa[i][j].waitingTime), True, NEGRO) 
                    x = i*self.tamCelda + 5
                    y = j*self.tamCelda + 5
                    self.pantalla.blit(txt, [x, y])
                elif(isinstance(self.mapa[i][j], Visitor)):
                    pygame.draw.ellipse(self.pantalla, NEGRO, [i*self.tamCelda, j*self.tamCelda, self.tamCelda, self.tamCelda], 5)
        pygame.display.flip()
        self.reloj.tick(60)
        return False










if(__name__ == "__main__"):

    dimensiones = [1000,1000]
    origen = [50, 50]
    tamCelda = (dimensiones[0] - origen[0])/20

    # ====================================================================



    mapa = [ [0 for j in range(20)] for i in range(20)]
    # habria que meter los datos del mapa con magia


    pygame.init()
    pantalla = pygame.display.set_mode(dimensiones) 
    pygame.display.set_caption("Mapa")
    hecho = False
    reloj = pygame.time.Clock()

    fuenteCuad = pygame.font.Font(None, 30) # fuente para los numeros de la cuadricula
    fuenteCola = pygame.font.Font(None, 75) # fuente para los numeros de la cola


    while not hecho:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                hecho = True

        # ---------------------------------------------------LÓGICA---------------------------------------------------
        
        # aqui se actualizaria el mapa
        # para optimizar puede esperar aqui a que haya alguna actualizacion
        # el programa puede parar indefinidamente y la ventana sigue sacando lo mismo

        # ---------------------------------------------------DIBUJO---------------------------------------------------

        pantalla.fill(BLANCO)


        # se pintan los colores de los cuadrantes (por casualidad el logo de windows)
        pygame.draw.rect(pantalla, CUAD1, [origen[0],             origen[1],             tamCelda*10, tamCelda*10])
        pygame.draw.rect(pantalla, CUAD2, [origen[0]+tamCelda*10, origen[1],             tamCelda*10, tamCelda*10])
        pygame.draw.rect(pantalla, CUAD3, [origen[0],             origen[1]+tamCelda*10, tamCelda*10, tamCelda*10])
        pygame.draw.rect(pantalla, CUAD4, [origen[0]+tamCelda*10, origen[1]+tamCelda*10, tamCelda*10, tamCelda*10])

        # se dibuja la cuadricula
        for i in range(20):
            pygame.draw.line(pantalla, NEGRO, [origen[0]+i*tamCelda, origen[1]], [origen[0]+i*tamCelda, dimensiones[1]], 3)
            pygame.draw.line(pantalla, NEGRO, [origen[0], origen[1]+i*tamCelda], [dimensiones[0], origen[1]+i*tamCelda], 3)

    
    
        # se escriben los numeros de la cuadricula
        pV0 = [origen[0]-tamCelda*0.6, origen[1]+tamCelda/2]
        pH0 = [origen[0]+tamCelda/2, origen[1]-tamCelda*0.5]

        for i in range(20):
            txt = fuenteCuad.render(str(i+1), True, NEGRO)
    
            pantalla.blit(txt, [pV0[0], pV0[1] + i*tamCelda])
            pantalla.blit(txt, [pH0[0] + i*tamCelda, pH0[1]])

        

        # se imprimen las cosas del mapa

        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()





