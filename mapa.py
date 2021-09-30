import pygame
import random
from time import sleep

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

dimensiones = [1000,1000]
origen = [100, 100]
tamCelda = (dimensiones[0] - origen[0])/20

# ====================================================================



mapa = [ [0 for j in range(20)] for i in range(20)]
# habria que meter los datos del mapa con magia


pygame.init()
pantalla = pygame.display.set_mode(dimensiones) 
pygame.display.set_caption("Mapa")
hecho = False
reloj = pygame.time.Clock()

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

    pygame.draw.rect(pantalla, CUAD1, [origen[0],             origen[1],             tamCelda*10, tamCelda*10])
    pygame.draw.rect(pantalla, CUAD2, [origen[0]+tamCelda*10, origen[1],             tamCelda*10, tamCelda*10])
    pygame.draw.rect(pantalla, CUAD3, [origen[0],             origen[1]+tamCelda*10, tamCelda*10, tamCelda*10])
    pygame.draw.rect(pantalla, CUAD4, [origen[0]+tamCelda*10, origen[1]+tamCelda*10, tamCelda*10, tamCelda*10])

    for i in range(20):
        pygame.draw.line(pantalla, NEGRO, [origen[0]+i*tamCelda, origen[1]], [origen[0]+i*tamCelda, dimensiones[1]], 3)
        pygame.draw.line(pantalla, NEGRO, [origen[0], origen[1]+i*tamCelda], [dimensiones[0], origen[1]+i*tamCelda], 3)


    # imprimir las cosas del mapa

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
