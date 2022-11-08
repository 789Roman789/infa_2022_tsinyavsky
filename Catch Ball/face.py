import pygame
from pygame.draw import *
import math
pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((50, 50, 50))

def drawAngry(x0, y0, size):
    circle(screen, (199, 199, 0), (x0, y0), size)
    rect(screen, (0, 0, 0), (x0 - size *0.5, y0 + size *0.5, size, size * 0.2))
    circle(screen, (240, 0, 0), (x0 - size * 0.4, y0 - size*0.25), size * 0.2)
    circle(screen, (0, 0, 0), (x0 - size * 0.4, y0 - size*0.26), size * 0.09)
    circle(screen, (240, 0, 0), (x0 + size * 0.4, y0 - size*0.3), size * 0.15)
    circle(screen, (0, 0, 0), (x0 + size * 0.4, y0 - size*0.3), size * 0.07)
    
    line(screen, (0, 0, 0), (x0 - size * 0.2, y0 - size*0.5), (x0 - size * 0.75, y0 - size*0.7), int(size * 0.15))
    line(screen, (0, 0, 0), (x0 + size * 0.1, y0 - size*0.4), (x0 + size * 0.65, y0 - size*0.6), int(size * 0.15))

#drawAngry(200, 200, 100)

pygame.display.update()
clock = pygame.time.Clock()
finished = False
xt = -110

while not finished:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            dx = x - 200
            dy = y - 200
            if(dx*dx+dy*dy < 100*100):
                print("On")
            
    screen.fill((50, 50, 50))
    drawAngry(200, 200, 100)
    xt += 50/FPS
    if(xt > 500):
        xt = 0
    pygame.display.update()

pygame.quit()