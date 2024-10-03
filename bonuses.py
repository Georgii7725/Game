import pygame
from circle import Circle

pygame.init()

colors_for_bonuses = {
    0: (0, 128, 255),
    1: (128, 0, 255),
    2: (200, 255, 128),
    3: (70, 70, 70),
    4: (70, 70, 70)
}

def create_bonus(tup, type) -> Circle:
    x0,y0 = tup
    bonus = Circle(x0-8, y0-8, 30)
    bonus.color = colors_for_bonuses[type]
    bonus.vx = 0
    bonus.vy = 6
    bonus.type = type
    return bonus    

class ContiniousBuff:
    applyed = False
    start = 0
    duration = 0
    def __init__(self, duration_of_buff, image):
        self.duration_of_buff = duration_of_buff
        self.image = image
    
    def execute(self):
        self.applyed = True
        self.start = pygame.time.get_ticks()
        self.duration = self.duration_of_buff

    def update(self):
        self.duration += self.duration_of_buff
        
    def return_state(self):
        self.applyed = False
    
    def rest_time(self):
        return self.start + self.duration - pygame.time.get_ticks()


class Extend_platform(ContiniousBuff):
    k = 1.4        
    
    def execute(self, n, platform: pygame.Rect):
        super().execute()
        k = self.k
        if platform.left - (k - 1) / 2 * platform.width < 0:
            platform.x, platform.width = 0, k*platform.width
        elif platform.right + (k - 1) / 2 * platform.width > n:        
            platform.x, platform.width = n - k*platform.width, k*platform.width
        else:
            platform.x, platform.width = platform.left - (k-1)/2*platform.width, k*platform.width
        
    def return_state(self, platform: pygame.Rect):
        super().return_state()
        k = self.k
        platform.x, platform.width = platform.left + (1-1/k)/2*platform.width, platform.width/k

class Slower(ContiniousBuff):
    k = 1.5
    
    def execute(self, ball: Circle):
        super().execute()
        ball.vx /= self.k
        ball.vy /= self.k
        
    def return_state(self, ball: Circle):
        super().return_state()
        ball.vx *= self.k
        ball.vy *= self.k

    
class Movement(ContiniousBuff):
    step = 4
    def return_state(self, m, platform):
        super().return_state()
        platform.y = 0.95 * m