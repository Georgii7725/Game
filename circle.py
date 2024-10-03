import pygame
from random import uniform, randint

pygame.init()
class Circle(pygame.Rect):
    type = -1
    # Нормальное значение от 5 до 12
    level = 9
    def __init__(self, iniX, iniY, length):
        self.radius = length // 2
        super().__init__(iniX-length//2,iniY-length//2,length,length)
        self.vy = uniform(-self.level, -self.level+1)
        self.vx = (2*randint(0, 1)-1)*((self.level**2 - self.vy**2)**0.5)
        self.color = (200, 50, 50)
    
    def revive(self, n, m):
        self.x, self.y = n//2, m//2
        self.vy = - abs(self.vy)
        
    def shift(self):
        self.x += self.vx
        self.y += self.vy

    def reflectX(self, buff):
        level = self.level / buff.k if buff.applyed else self.level
        self.vy = min(level-1, max(-level+1, self.vy + randint(-1, 1)))
        self.vx = -1 * self.vx // abs(self.vx) * ((level**2 - self.vy**2)**0.5)
        
    def reflectY(self, buff):
        level = self.level / buff.k if buff.applyed else self.level
        self.vx = min(level-1, max(-level+1, self.vx + randint(-1, 1)))
        self.vy = -1 * self.vy // abs(self.vy) * ((level**2 - self.vx**2)**0.5)