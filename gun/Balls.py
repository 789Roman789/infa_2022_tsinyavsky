import pygame
from config import *
from random import choice
from Target import Target
from abc import ABC, abstractmethod


class Ball(ABC):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 7

    @abstractmethod
    def move(self):
        pass

    def isAlive(self):
        '''
        Проверяет жив ли мяч
        '''
        return self.live > 0

    def TickTime(self):
        '''
        Отсчитывает время до смерти
        '''

        self.live -= 1/FPS

    @abstractmethod
    def draw(self):
        pass

    def hittest(self, targ: Target):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            targ: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        dx = self.x - targ.x
        dy = self.y - targ.y
        dsq = dx*dx+dy*dy

        return dsq <= (targ.r+self.r)**2


class Ball0(Ball):
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.TickTime()

        self.x += self.vx/FPS
        self.y -= self.vy/FPS
        if self.y + self.r >= FLOOR:
            vy0 = abs(self.vy)
            self.vy = vy0*BOUNCE

            if (self.vy < 10):
                self.vy = 0
            if (abs(self.vx) >= 5):
                self.vx -= min(abs(self.vx), vy0*(BOUNCE+1) *
                               FRICTION) * abs(self.vx)/self.vx
            else:
                self.vx = 0

        else:
            self.vy = self.vy*(1-AFRI) - 300/FPS
            self.vx *= 1-AFRI
        if self.x + self.r >= self.screen.get_width():
            self.vx = -abs(self.vx)
        if self.x - self.r <= 0:
            self.vx = abs(self.vx)


class Ball1(Ball):
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            (200, 210, 240),
            (self.x, self.y),
            self.r/2
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """

        self.TickTime()

        self.x += self.vx/FPS
        self.y -= self.vy/FPS
        if self.y + self.r >= FLOOR:
            vy0 = abs(self.vy)
            self.vy = vy0*BOUNCE

            if (self.vy < 10):
                self.vy = 0
            if (abs(self.vx) >= 5):
                self.vx -= min(abs(self.vx), vy0*(BOUNCE+1) *
                               FRICTION) * abs(self.vx)/self.vx
            else:
                self.vx = 0

        else:
            self.vy = self.vy*(1-AFRI) + 50/FPS
            self.vx *= 1-AFRI
        if self.x + self.r >= self.screen.get_width():
            self.vx = -abs(self.vx)
        if self.x - self.r <= 0:
            self.vx = abs(self.vx)
