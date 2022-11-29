import math
import random
import pygame
from config import *
from abc import ABC, abstractmethod


class Target(ABC):
    def __init__(self, screen):
        self.points = 0
        self.live = 1
        self.new_target()
        self.vx = [0 for i in range(60)]
        self.vy = [0 for i in range(60)]
        self.viter = 0
        self.screen = screen

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = random.uniform(550, 780)
        self.y = random.uniform(250, 450)
        self.r = random.uniform(10, 50)
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass


class Target0(Target):
    def draw(self):
        self.update()
        x0 = self.x
        y0 = self.y

        size = self.r
        pygame.draw.circle(self.screen, (199, 199, 0), (x0, y0), size)
        pygame.draw.rect(self.screen, (0, 0, 0), (x0 - size *
                         0.5, y0 + size * 0.5, size, size * 0.2))
        pygame.draw.circle(self.screen, (240, 0, 0),
                           (x0 - size * 0.4, y0 - size*0.25), size * 0.2)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (x0 - size * 0.4, y0 - size*0.26), size * 0.09)
        pygame.draw.circle(self.screen, (240, 0, 0),
                           (x0 + size * 0.4, y0 - size*0.3), size * 0.15)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (x0 + size * 0.4, y0 - size*0.3), size * 0.07)

        pygame.draw.line(self.screen, (0, 0, 0), (x0 - size * 0.2, y0 -
                         size*0.5), (x0 - size * 0.75, y0 - size*0.7), int(size * 0.15))
        pygame.draw.line(self.screen, (0, 0, 0), (x0 + size * 0.1, y0 -
                         size*0.4), (x0 + size * 0.65, y0 - size*0.6), int(size * 0.15))

    def update(self):
        phi = random.uniform(0, 2*math.pi)
        r = random.uniform(200, 700)
        self.vx[self.viter] = math.cos(phi) * r
        self.vy[self.viter] = math.sin(phi) * r
        self.viter = (self.viter + 1) % min(len(self.vx), len(self.vy))
        vx = sum(self.vx) / len(self.vx)
        vy = sum(self.vy) / len(self.vy)
        x0 = self.x + vx / FPS
        y0 = self.y + vy / FPS
        if x0 + self.r > self.screen.get_width():
            x0 = self.screen.get_width() - self.r
        if x0 - self.r < 0:
            x0 = self.r
        if y0 + self.r > FLOOR:
            y0 = FLOOR - self.r
        if y0 - self.r < 0:
            y0 = self.r
        self.x = x0
        self.y = y0


class Target1(Target):
    def draw(self):
        self.update()
        x0 = self.x
        y0 = self.y

        size = self.r
        pygame.draw.circle(self.screen, (199, 199, 0), (x0, y0), size)

    def update(self):
        pass
