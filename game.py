import pygame
from pygame.draw import *
from random import randint, uniform
import numpy as np
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))

RED = (255, 100, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def getVel():
    vx = randint(-50, 50)
    vy = randint(-50, 50)
    
    return [vx, vy]

def getRandom():
    x0 = randint(100, 1100)
    y0 = randint(100, 900)
    size = randint(20, 100)
    color = randint(0, 5)
    return (x0, y0, size, color)

def drawAngry(x0, y0, size, c):
    color = COLORS[c]
    circle(screen, color, (x0, y0), size)
    rect(screen, (0, 0, 0), (x0 - size *0.5, y0 + size *0.5, size, size * 0.2))
    circle(screen, (240, 0, 0), (x0 - size * 0.4, y0 - size*0.25), size * 0.2)
    circle(screen, (0, 0, 0), (x0 - size * 0.4, y0 - size*0.26), size * 0.09)
    circle(screen, (240, 0, 0), (x0 + size * 0.4, y0 - size*0.3), size * 0.15)
    circle(screen, (0, 0, 0), (x0 + size * 0.4, y0 - size*0.3), size * 0.07)
    
    line(screen, (0, 0, 0), (x0 - size * 0.2, y0 - size*0.5), (x0 - size * 0.75, y0 - size*0.7), int(size * 0.15))
    line(screen, (0, 0, 0), (x0 + size * 0.1, y0 - size*0.4), (x0 + size * 0.65, y0 - size*0.6), int(size * 0.15))


def new_ball():
    '''рисует новый шарик '''
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

pygame.display.update()
clock = pygame.time.Clock()
finished = False


balls = []
poses = []
vels = []
lives = []

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
    
    (x, y, s, c) = getRandom()        
    balls.append((s, c))
    liv = uniform(1.5, 5)
    poses.append([x,y,0,liv])
    vels.append(getVel())
    lives.append(liv)
    
    rng = range(len(balls)-1, 0, -1)
    
    for i in rng:
        poses[i][3] -= 1/FPS
        if(poses[i][3] < 1):
            poses[i][2] = balls[i][0] * poses[i][3]
        elif((lives[i]- poses[i][3]) < 1):
            poses[i][2] = balls[i][0] * (lives[i] - poses[i][3]) 
        else:
            poses[i][2] = balls[i][0]
        if(lives[i] <= 0):
            del lives[i]
            del balls[i]
            del poses[i]
            del vels[i]
    
    for i in range(len(balls)):
        (size, color) = balls[i]
        poses[i][0] += vels[i][0] / FPS
        poses[i][1] += vels[i][1] / FPS
        (x0, y0, s, lt) = poses[i]
        drawAngry(x0, y0, s, color)
    
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()