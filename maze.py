from pygame import *
from sys import exit
from time import sleep


class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y


   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
       if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_DOWN] and self.rect.y < win_height - 80:
           self.rect.y += self.speed

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"


        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_width, wall_height, wall_x, wall_y):
        super().__init__()
        self.color_1 = color_1
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x=wall_x
        self.rect.y=wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class EnemyWall(Wall):
    direction = "left"
    def update(self):
        if self.rect.x <= 230:
            self.direction = "right"
        if self.rect.x >= 470:
            self.direction = "left"


        if self.direction == "left":
            self.rect.x -= 2
        else:
            self.rect.x += 2


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))



player = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)
'''wall: r,g,b,width,height,x,y'''
wall1=Wall(200, 200, 200, 30, win_height-100, 230, 0)
wall2=Wall(200, 200, 200, 30, 600, 470, 600-win_height)
wall3=EnemyWall(200, 200, 200, 10, 100, 470, 0)
wall4=EnemyWall(200, 200, 200, 10, 100, 600, 100)
wall5=EnemyWall(200, 200, 200, 10, 100, 470, 200)
wall6=EnemyWall(200, 200, 200, 10, 100, 600, 300)
game = True
finish = False
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()
money = mixer.Sound("money.ogg")
kick = mixer.Sound("kick.ogg")
font.init()
font = font.SysFont('Arial', 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))
while game:
     for e in event.get():
        if e.type == QUIT:
            game = False
    
     if finish != True:
         window.blit(background,(0, 0))
         player.update()
         monster.update()
        
         player.reset()
         monster.reset()
         final.reset()
        
         wall1.draw_wall()
         wall2.draw_wall()
         wall3.draw_wall()
         wall4.draw_wall()
         wall5.draw_wall()
         wall6.draw_wall()
         wall3.update()
         wall4.update()
         wall5.update()
         wall6.update()
         if sprite.collide_rect(player, monster) or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall2) or sprite.collide_rect(player, wall3) : #...?
             finish=True
             window.blit(lose, (200, 200))
             sleep(2)
         if sprite.collide_rect(player, final):
             window.blit(win, (200, 200))
             finish=True
             money.play()
             sleep(1)
             sleep(3)
    
     if finish == True:
        sleep(0)
        exit()
     display.update()
     clock.tick(FPS)