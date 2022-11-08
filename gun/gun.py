import math
from random import choice
import random
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

FLOOR = 500
BOUNCE = 0.75
FRICTION = 0.08
AFRI = 0.012

def lerp(a:pygame.Color,b:pygame.Color, t):
    t = min(max(t, 0),1)
    c = pygame.Color(int(a.r*(1-t) + b.r * t), int(a.g*(1-t) + b.g * t), int(a.b*(1-t) + b.b * t))
    return c


class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        self.new_target()
        

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = random.uniform(550, 780)
        self.y = random.uniform(250, 450)
        self.r = random.uniform(10, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        x0 = self.x
        y0 = self.y
        size = self.r
        pygame.draw.circle(screen, (199, 199, 0), (x0, y0), size)
        pygame.draw.rect(screen, (0, 0, 0), (x0 - size *0.5, y0 + size *0.5, size, size * 0.2))
        pygame.draw.circle(screen, (240, 0, 0), (x0 - size * 0.4, y0 - size*0.25), size * 0.2)
        pygame.draw.circle(screen, (0, 0, 0), (x0 - size * 0.4, y0 - size*0.26), size * 0.09)
        pygame.draw.circle(screen, (240, 0, 0), (x0 + size * 0.4, y0 - size*0.3), size * 0.15)
        pygame.draw.circle(screen, (0, 0, 0), (x0 + size * 0.4, y0 - size*0.3), size * 0.07)
        
        pygame.draw.line(screen, (0, 0, 0), (x0 - size * 0.2, y0 - size*0.5), (x0 - size * 0.75, y0 - size*0.7), int(size * 0.15))
        pygame.draw.line(screen, (0, 0, 0), (x0 + size * 0.1, y0 - size*0.4), (x0 + size * 0.65, y0 - size*0.6), int(size * 0.15))
        

class Ball:
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
            
            if(self.vy < 10):
                self.vy = 0
            if(abs(self.vx) >= 5):
                self.vx -= min(abs(self.vx), vy0*(BOUNCE+1)*FRICTION) * abs(self.vx)/self.vx
            else:
                self.vx = 0
            
        else:
            self.vy = self.vy*(1-AFRI) - 300/FPS
            self.vx *= 1-AFRI
        if self.x + self.r >= self.screen.get_width():
            self.vx = -abs(self.vx)
        if self.x - self.r <= 0:
            self.vx = abs(self.vx)
            
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


    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, targ : Target):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            targ: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        
        dx  = self.x - targ.x
        dy = self.y - targ.y
        dsq = dx*dx+dy*dy
        
        return dsq <= (targ.r+self.r)**2


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
        new_ball = Ball(self.screen)
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
            if(event.pos[0] - 20) > 0:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
                self.an =  max(min(self.an, math.pi*0.4), -math.pi * 0.4)

    def draw(self):
        x0 = 20
        y0 = 450
        
        dx0 = 5 * math.sin(self.an)
        dy0 = -5 * math.cos(self.an)
        
        t = (self.f2_power-self.powerMin)/(self.powerMax - self.powerMin)
        
        dx1 = (30+50*t) * math.cos(self.an)
        dy1 = (30+50*t) * math.sin(self.an)
        
        color = lerp(pygame.color.Color(self.color), pygame.color.Color(self.clcColor), t)
        
        pygame.draw.polygon(self.screen, color, [[x0-dx0,y0-dy0],[x0+dx0,y0+dy0],[x0+dx0+dx1,y0+dy0+dy1],[x0-dx0+dx1,y0-dy0+dy1]])

    def power_up(self):
        if self.f2_on:
            if self.f2_power < self.powerMax:
                self.f2_power += self.recharge / FPS





pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
        
    pygame.draw.rect(screen, (60,160,80), [[0,FLOOR],[WIDTH,HEIGHT]])    
    
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
        if not(b.isAlive()):
            balls.remove(b)
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
