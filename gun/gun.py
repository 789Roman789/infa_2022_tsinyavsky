import math
from random import uniform
from config import *
from Balls import Ball, Ball0, Ball1
from Target import Target, Target0, Target1

import pygame


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def lerp(a: pygame.Color, b: pygame.Color, t):
    t = min(max(t, 0), 1)
    c = pygame.Color(int(a.r*(1-t) + b.r * t),
                     int(a.g*(1-t) + b.g * t), int(a.b*(1-t) + b.b * t))
    return c


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.powerMin = 150
        self.powerMax = 1000
        self.recharge = 1000
        self.f2_power = self.powerMin
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.clcColor = RED

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        rv = uniform(0, 1)
        if (rv < 0.3):
            new_ball = Ball1(self.screen)
        else:
            new_ball = Ball0(self.screen)
        new_ball.r += 5
        #self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = self.powerMin

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0] - 20) > 0:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
                self.an = max(min(self.an, math.pi*0.4), -math.pi * 0.4)

    def draw(self):
        x0 = 20
        y0 = 450

        dx0 = 5 * math.sin(self.an)
        dy0 = -5 * math.cos(self.an)

        t = (self.f2_power-self.powerMin)/(self.powerMax - self.powerMin)

        dx1 = (30+50*t) * math.cos(self.an)
        dy1 = (30+50*t) * math.sin(self.an)

        color = lerp(pygame.color.Color(self.color),
                     pygame.color.Color(self.clcColor), t)

        pygame.draw.polygon(self.screen, color, [
                            [x0-dx0, y0-dy0], [x0+dx0, y0+dy0], [x0+dx0+dx1, y0+dy0+dy1], [x0-dx0+dx1, y0-dy0+dy1]])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < self.powerMax:
                self.f2_power += self.recharge / FPS


bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
targets = [Target0(screen), Target0(screen), Target1(screen)]
finished = False

while not finished:
    screen.fill((235, 235, 255))
    gun.draw()
    for target in targets:
        target.draw()
    for b in balls:
        b.draw()

    pygame.draw.rect(screen, (60, 160, 80), [[0, FLOOR], [WIDTH, HEIGHT]])

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls[::-1]:
        b.move()
        if not (b.isAlive()):
            balls.remove(b)
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
    gun.power_up()

pygame.quit()
