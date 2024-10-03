import pygame
from bonuses import *
from circle import Circle
from random import randint

pygame.init()

n, m = 1000, 700
screen = pygame.display.set_mode((n, m))
done = False

number_of_lifes = 5
life = pygame.transform.scale(pygame.image.load("Жизнь.jpg"), (27, 27))
clock = pygame.time.Clock()
ball_radius = 10
ball = Circle(n//2,m//2, 2*ball_radius)
platform = pygame.Rect(n//2, 0.95 * m, n // 8, m // 35)        
tiles = [pygame.Rect(50*n//(6*n+50) + (300*n // (6*n+50))*i, 30+20*j, 250*n // (6*n + 50), 10) for i in range(10*n//500) for j in range(4)]
bonuses = []
size = (45, 45)
buff_extend_platform = Extend_platform(duration_of_buff=3000, image=pygame.transform.scale(pygame.image.load("extend.png"), size))
buff_slower = Slower(                  duration_of_buff=6000, image=pygame.transform.scale(pygame.image.load("slower.png"), size))
buff_reverse = ContiniousBuff(         duration_of_buff=5000, image=pygame.transform.scale(pygame.image.load("reverse.png"), size))
buff_movement = Movement(              duration_of_buff=4000, image=pygame.transform.scale(pygame.image.load("movement.png"), size))


while not done:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

######################################################  Прорисовка объектов  ###################################################### 
    for i in range(number_of_lifes): screen.blit(life, (25*i, 0))
    for tile in tiles: pygame.draw.rect(screen, (128, 128, 128), tile)
    pygame.draw.rect(screen, (0,0,0), platform)
    for bonus in bonuses:
        pygame.draw.circle(screen, bonus.color, bonus.center, bonus.radius)
        if bonus.bottom > m: bonuses.remove(bonus)
        bonus.shift()
    for i, buff in enumerate(list(filter(lambda b: b.rest_time() > 0, [buff_extend_platform, buff_slower, buff_reverse, buff_movement]))): 
        screen.blit(buff.image, (n-150, 200+70*i))
        screen.blit(pygame.font.SysFont('arial', 20, bold=True).render(str(buff.rest_time()//100/10), True, (0, 0, 0)), (n-50, 220+70*i)) #FIXME
    pygame.draw.circle(screen, ball.color, ball.center, ball.radius)

########################################################  Конец игры  ######################################################
    if number_of_lifes == 0:
        text_surface = pygame.font.SysFont(None, 80).render("LOSS", True, (255, 0, 0))
        screen.blit(text_surface, (5*n//12, m/2))
        pygame.display.flip()
        continue
    if len(tiles) == 0:
        text_surface = pygame.font.SysFont(None, 80).render("WIN", True, (255, 0, 0))
        screen.blit(text_surface, (5*n//12, m/2))
        pygame.display.flip()
        continue
        
######################################################  Сдвиг платформы  ######################################################
    ### Сдвиг по горизонтали
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:  platform.x = min(n-platform.width, max(0, platform.x - 5)) if not buff_reverse.applyed else min(n-platform.width, max(0, platform.x + 5))
    if pressed[pygame.K_RIGHT]: platform.x = min(n-platform.width, max(0, platform.x + 5)) if not buff_reverse.applyed else min(n-platform.width, max(0, platform.x - 5))
    ### Сдвиг по вертикали
    if buff_movement.applyed:    
        if platform.y > 0.95 * m + 2: buff_movement.step *= -1
        if platform.y < 0.75*m: buff_movement.step *= -1
        platform.y += buff_movement.step

###############################################  Движение шарика  ##################################################
    ball.shift()
    if ball.top < 30 and ball.top - ball.vy > 29:
        ball.reflectY(buff_slower) 
    if ball.left < 0 and ball.left - ball.vx > -1 or ball.right > n and ball.right - ball.vx < n+1:
        ball.reflectX(buff_slower)
    if ball.centery > platform.bottom:
        ball.revive(n, m)
        # platform.x = n//2        Если хотим после смерти возврщать платформу на место
    if ball.colliderect(platform) and ball.vy > 0:
        ball.reflectY(buff_slower)
        
    delete_index = ball.collidelist(tiles)
    if delete_index != -1:
        type = randint(0, 4)
        if type < 5:
            bonus = create_bonus(tiles[delete_index].center,type)
            bonuses.append(bonus)
        if ball.centerx + ball_radius // 2 < tiles[delete_index].left or ball.centerx - ball_radius // 2> tiles[delete_index].right: ball.reflectX(buff_slower)
        else: ball.reflectY(buff_slower)
        tiles.pop(delete_index)

###########################################  Проверка пересечения с летящими бонусами  ######################################################
    trash = platform.collidelistall(bonuses)
    for i in trash:
        match bonuses[i].type:
            case 0:
                if buff_extend_platform.applyed:
                    buff_extend_platform.update()
                else:
                    buff_extend_platform.execute(n, platform)
            case 1:
                if buff_slower.applyed:
                    buff_slower.update()
                else:
                    buff_slower.execute(ball)
            case 2:
                number_of_lifes += 1
            case 3:
                if buff_reverse.applyed:
                    buff_reverse.update()
                else:
                    buff_reverse.execute()
            case 4:
                if buff_movement.applyed:
                    buff_movement.update()
                else:
                    buff_movement.execute()
    for i in sorted(trash, reverse=True): bonuses.pop(i)


###################################################  Проверка действия бафов  ################################################################
    for buff in [buff_extend_platform, buff_slower, buff_reverse, buff_movement]:
        if buff.applyed and buff.rest_time() <= 0:
            if isinstance(buff, Extend_platform):
                buff.return_state(platform)
            elif isinstance(buff, Slower):
                buff.return_state(ball)
            elif isinstance(buff, Movement):
                buff.return_state(m, platform)
            else:
                buff.return_state()
    
    clock.tick(60)
    pygame.display.flip()