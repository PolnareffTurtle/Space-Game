import pygame
from sys import exit
from random import randint, choice, uniform
from savedata import *

pygame.init()
bg_music = pygame.mixer.Sound('audio/space.wav')
bg_music.set_volume(0.5)
bg_music.play(-1)

screen = pygame.display.set_mode((1280,720))
skins_list = [pygame.transform.rotozoom(pygame.image.load(f'graphics/spaceship/spaceship{i}.png').convert_alpha(),0,0.5) for i in range(1,5)]
game_time_index = 0

class Player(pygame.sprite.Sprite):
    def __init__(self,index):
        super().__init__()
        self.image = skins_list[index]
        self.ref =self.image
        self.rect = self.image.get_rect(midleft = (200,400))
        self.gravity = 0
        self.radius = 0.7 * self.rect.width/2

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity += -0.6
        else:
            self.gravity += 0.5

    def apply_gravity(self):
        #max and min for gravity
        if self.gravity > 10+game_time_index: self.gravity = 10+game_time_index
        if self.gravity < -10-game_time_index: self.gravity = -10-game_time_index
        self.rect.y += self.gravity
        #max and min for position
        if self.rect.top < 20: self.rect.top,self.gravity = 20,0
        if self.rect.bottom > 700: self.rect.bottom,self.gravity = 700,0
        self.image = pygame.transform.rotozoom(self.ref,-self.gravity,1)

    def update(self):
        self.player_input()
        self.apply_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type): #TODO: create different types for the obstacles --> def __init__(self,type)
        super().__init__()
        self.type = type
        if self.type == 'asteroid':
            self.size = uniform(0.3,0.5)
            self.speed = randint(2+int(game_time_index),4+int(game_time_index))
            self.angle = uniform(-2,2)
            self.image = pygame.image.load(f'graphics/asteroid/asteroid{randint(1,10)}.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,self.size)
            self.rect = self.image.get_rect(midleft = (randint(1300,1500),randint(20,700)))
            self.radius = 0.8 * self.rect.height/2

        elif self.type == 'comet':
            self.speed = randint(5+int(game_time_index),7+int(game_time_index))
            self.image = pygame.image.load(f'graphics/comet.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,30,1)
            self.rect = self.image.get_rect(bottomleft = (randint(900,2400),randint(-200,-100)))
            self.radius = 50

        elif self.type == 'doge':
            self.speed = randint(5 + int(game_time_index), 7 + int(game_time_index))
            self.image = pygame.image.load(f'graphics/image-removebg-preview.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 30, 1)
            self.rect = self.image.get_rect(bottomleft=(randint(900, 2400), randint(-200, -100)))
            self.radius = 50

    def destroy(self):
        if self.rect.right < 0 or self.rect.top > 720 or (self.rect.bottom < 0 and self.type == 'asteroid'):
            self.kill()

    def update(self):
        if self.type in ['comet','doge']:
            self.rect.x += -2*self.speed
            self.rect.y += self.speed
        elif self.type == 'asteroid':
            self.rect.x += -self.speed
            self.rect.y += self.angle
            #self.image = pygame.transform.rotate(self.image,1)
            #self.index += 0.5
            #self.image = self.frames[int(self.index)%180]
        self.destroy()

class Text():
    def __init__(self,text,size,color,xpos,ypos,hover,key=None):
        self.key = key
        self.text = text
        self.color = color
        self.hover = hover
        self.center = (xpos,ypos)
        self.font = pygame.font.Font(None,size)
        self.font2 = pygame.font.Font(None,int(size*1.5))
        self.image = self.font.render(text,True,color)
        self.rect = self.image.get_rect(center=self.center)

    def text_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image = self.font2.render(self.text,True,self.color)
            self.rect = self.image.get_rect(center=self.center)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.image = self.font.render(self.text,True,self.color)
            self.rect = self.image.get_rect(center=self.center)

    def clicked(self,key=None):
        mousedown = pygame.mouse.get_pressed()[0]
        keydown = pygame.key.get_pressed()[key]
        if self.rect.collidepoint(pygame.mouse.get_pos()) and mousedown or keydown:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return True

    def text_blit(self):
        if self.hover:
            self.text_hover()
        screen.blit(self.image,self.rect)


class Button():
    def __init__(self,type):
        self.type = type
        if type == 'left':
            self.image = pygame.image.load('graphics/triangle_l.png').convert_alpha()
            self.rect = self.image.get_rect(midright = (450,300))
        else:
            self.image = pygame.image.load('graphics/triangle_r.png').convert_alpha()
            self.rect = self.image.get_rect(midleft = (850,300))
        self.ref = self.image

    def button_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.image = pygame.transform.rotozoom(self.ref,0,1.5)
            if self.type =='left':
                self.rect = self.image.get_rect(midright=(450,300))
            else:
                self.rect = self.image.get_rect(midleft=(850,300))
            return True
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.image = self.ref
            if self.type == 'left':
                self.rect = self.image.get_rect(midright=(450,300))
            else:
                self.rect = self.image.get_rect(midleft=(850,300))
            return False

    def clicked(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return True

    def button_blit(self):
        self.button_hover()
        screen.blit(self.image,self.rect)

def display_score():
    current_time = int(((pygame.time.get_ticks() - start_time) // 100)*(1+game_time_index))
    score_text = Text(f'Score: {current_time}',50,'White',1100,80,False)
    score_text.text_blit()
    return current_time

def collisions():
    if pygame.sprite.spritecollide(player.sprite,obstacles,False,collided=pygame.sprite.collide_circle):
        obstacles.empty()
        return False
    return True


pygame.display.set_caption('Asteroid Attack')
clock = pygame.time.Clock()
mainfont = pygame.font.Font(None, 50)
titlefont = pygame.font.Font(None,100)
biggerfont = pygame.font.Font(None,75)
game_active = False
start_time = 0
score = 0
skin_index = 2
meteor_shower_on = False
newgame=True

#background
bg_index=0
bg1 = pygame.image.load('graphics/background1.png').convert()
bg2 = pygame.image.load('graphics/background2.png').convert()

#--------------------------GROUPS-------------------------------------
player = pygame.sprite.GroupSingle()
player.add(Player(skin_index))

obstacles = pygame.sprite.Group()

#-----------------------------intro screen---------------------------------



title1 = Text('Asteroid Attack',100,'White',640,100,False)
title2 = Text('You Crashed!',100,'White',640,100,False)
instruction1 = Text('Play [r]',50,'Yellow',640,500,True,pygame.K_r)
instruction2 = Text('Play Again [r]',50,'Yellow',640,500,True,pygame.K_r)

#-------------------------------Timer---------------------------------------
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

#meteor shower
meteor_shower = pygame.USEREVENT + 2
pygame.time.set_timer(meteor_shower,40000)
meteor_start = 0
meteor_shower_text = Text('METEOR SHOWER',100,'#ff4576',640,300,False)

#character select
triangle_l = Button('left')
triangle_r = Button('right')

#main loop
while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if meteor_shower_on:

                if pygame.time.get_ticks()-meteor_start < 5000:
                    if event.type == obstacle_timer:
                        obstacles.add(Obstacle('comet'))
                        obstacles.add(Obstacle('comet'))
                else:
                    meteor_shower_on = False
            else:
                if event.type == obstacle_timer:
                    if randint(1, 100) == 1:
                        obstacles.add(Obstacle('doge'))
                    else:
                        obstacles.add(Obstacle(choice(['comet', 'asteroid', 'asteroid', 'asteroid'])))
                if event.type == meteor_shower:
                    meteor_start = pygame.time.get_ticks()
                    meteor_shower_on = True

        elif instruction1.clicked(key=pygame.K_r) or instruction2.clicked(key=pygame.K_r):
            newgame=True
            game_active = True
            start_time = pygame.time.get_ticks()
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if triangle_l.button_hover():
                    skin_index += -1
                    skin_index = skin_index % 4
                if triangle_r.button_hover():
                    skin_index += 1
                    skin_index = skin_index % 4

    #actual game
    if game_active:
        if newgame:
            player.add(Player(skin_index))
            newgame=False
        game_time_index+=0.001
        #----------------------background---------------------------
        if bg_index <=1280: screen.blit(bg1,(-bg_index, 0))
        else: screen.blit(bg1,(2560-bg_index,0))
        screen.blit(bg2, (1280 - bg_index, 0))
        bg_index += 1+int(game_time_index)
        bg_index = bg_index%2560

        if meteor_shower_on and pygame.time.get_ticks()-meteor_start < 2000:
            meteor_shower_text.text_blit()
        #player and obstacles
        player.draw(screen)
        player.update()

        obstacles.draw(screen)
        obstacles.update()

        score = display_score()

        game_active = collisions()

    #----------------------------home screen-------------------------------------
    else:
        # background
        if bg_index <= 1280: screen.blit(bg1, (-bg_index, 0))
        else: screen.blit(bg1, (2560 - bg_index, 0))
        screen.blit(bg2, (1280 - bg_index, 0))
        bg_index += 1
        bg_index = bg_index % 2560

        spaceship_title = pygame.transform.rotozoom(skins_list[skin_index], 30, 2)
        spaceship_title_rect = spaceship_title.get_rect(center=(640, 300))

        screen.blit(spaceship_title, spaceship_title_rect)
        triangle_l.button_blit()
        triangle_r.button_blit()

        game_time_index = 0
        player.sprite.gravity = 0
        player.sprite.rect.midleft = (200, 400)
        #-----------------------score--------------------------------------------
        if score == 0:
            title1.text_blit()

            if highscore > 0:
                highscore_text = Text(f'Highscore: {highscore}',50,'White',640,650,False)
                highscore_text.text_blit()
            instruction1.text_blit()
        else:
            title2.text_blit()
            if score > highscore:
                highscore = score
                f = open('savedata.py','w')
                f.write('highscore = '+str(highscore)+'\n')
                f.close()
            score_text = Text(f'Your Score: {score}', 50, 'White', 640, 600, False)
            highscore_text = Text(f'Highscore: {highscore}', 50, 'White', 640, 650, False)
            instruction2.text_blit()
            score_text.text_blit()
            highscore_text.text_blit()


    pygame.display.update()
    clock.tick(60)