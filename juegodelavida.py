import pygame
import numpy as np
import time


pygame.init()
width,height=500,500
screen=pygame.display.set_mode((height,width))
bg=25,25,25
screen.fill(bg)

nxC,nyC=30, 30
dimCW=width/nxC
dimCH=height/nyC

#Estado de las celdas. Vivas=1, Muertas =0
gameState=np.zeros((nxC,nyC))

#Inicializamos Estados de partida
pause=False

#automata palito
gameState[10,3]=1
gameState[10,4]=1
gameState[10,5]=1

#automata movil
gameState[21,21]=1
gameState[22,22]=1
gameState[22,23]=1
gameState[21,23]=1
gameState[20,23]=1

#bucle de ejecución
while True:
    newGameState=np.copy(gameState)
    #limpiamos la pantalla de informacion
    screen.fill(bg)
    time.sleep(0.1)

    ev=pygame.event.get()
    for event in ev:
        if event.type==pygame.KEYDOWN:
            pause=not pause
        if event.type == pygame.QUIT:
            pygame.quit()
            ##exit()
            
    if not pause:
        for y in range(0,nxC):
            for x in range(0,nyC):
                #Calculamos el número de vecinos cercanos
                n_vecinos=gameState[(x-1)%nxC,(y-1)%nyC]+\
                          gameState[(x)%nxC,(y-1)%nyC]+\
                          gameState[(x+1)%nxC,(y-1)%nyC]+\
                          gameState[(x-1)%nxC,(y)%nyC]+\
                          gameState[(x+1)%nxC ,(y)%nyC]+\
                          gameState[(x-1)%nxC,(y+1)%nyC]+\
                          gameState[(x)%nxC,(y+1)%nyC]+\
                          gameState[(x+1)%nxC,(y+1)%nyC]

                #Regla 1: Una celula muerta con 3 vecinos vivos resucita
                if gameState[x,y]==0 and n_vecinos==3:
                    newGameState[x,y]=1
                #Regla 2: Una celula viva con más o menos de 3 vecinos vivos muere
                elif gameState[x,y]==1 and (n_vecinos<2 or n_vecinos>3):
                    newGameState[x,y]=0
                #creamos el poligono para cada celda a dibujar
                poly=[(x*dimCW,y*dimCH),
                    ((x+1)*dimCW,y*dimCH),
                    ((x+1)*dimCW,(y+1)*dimCH),
                    (x*dimCW,(y+1)*dimCH)]
                #pintamos las celdas segun corresponda
                if newGameState[x,y]==0:
                    pygame.draw.polygon(screen,(128,128,128),poly,1)
                else:
                    pygame.draw.polygon(screen,(255,255,255),poly,0)
        #Actualizamos el estado del juego
        gameState=np.copy(newGameState)

        pygame.display.flip()
