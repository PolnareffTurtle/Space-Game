import pygame
from sys import exit
from random import randint, choice, uniform
from savedata import *

pygame.init()
screen = pygame.display.set_mode((1280,720))
spaceship = pygame.transform.rotozoom(pygame.image.load('graphics/spaceship.png').convert_alpha(),0,0.5)
game_time_index = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship
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
        self.image = pygame.transform.rotozoom(spaceship,-self.gravity,1)

    def update(self):
        self.player_input()
        self.apply_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type): #TODO: create different types for the obstacles --> def __init__(self,type)
        super().__init__()
        self.type = type
        if self.type == 'asteroid':
            self.speed = randint(2+int(game_time_index),4+int(game_time_index))
            self.angle = uniform(-2,2)
            self.image = pygame.image.load(f'graphics/asteroid/asteroid{randint(1,10)}.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,0.4)
            self.rect = self.image.get_rect(midleft = (randint(1300,1500),randint(20,700)))
            self.radius = 0.8 * self.rect.height/2

        elif self.type == 'comet':
            self.speed = randint(5+int(game_time_index),7+int(game_time_index))
            self.image = pygame.image.load('graphics/comet.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,30,1)
            self.rect = self.image.get_rect(bottomleft = (randint(900,2400),randint(-200,-100)))
            self.radius = 50
    def destroy(self):
        if self.rect.right < 0 or self.rect.top > 720 or (self.rect.bottom < 0 and self.type == 'asteroid'):
            self.kill()

    def update(self):
        if self.type == 'comet':
            self.rect.x += -2*self.speed
            self.rect.y += self.speed
        elif self.type == 'asteroid':
            self.rect.x += -self.speed
            self.rect.y += self.angle
            #self.image = pygame.transform.rotate(self.image,1)
            #self.index += 0.5
            #self.image = self.frames[int(self.index)%180]
        self.destroy()

def display_score():
    current_time = int(((pygame.time.get_ticks() - start_time) // 100)*(1+game_time_index))
    score_surf = mainfont.render(f'Score: {current_time}', True, 'White')
    score_rect = score_surf.get_rect(topright = (1230,50))
    screen.blit(score_surf, score_rect)
    return current_time

def collisions():
    if pygame.sprite.spritecollide(player.sprite,obstacles,False,collided=pygame.sprite.collide_circle):
        obstacles.empty()
        return False
    return True


pygame.display.set_caption('Space Game')
clock = pygame.time.Clock()
mainfont = pygame.font.Font(None, 50)
titlefont = pygame.font.Font(None,100)
game_active = False
start_time = 0
score = 0
meteor_shower_on = False

#background
bg_index=0
bg1 = pygame.image.load('graphics/background1.png').convert()
bg2 = pygame.image.load('graphics/background2.png').convert()

#--------------------------GROUPS-------------------------------------
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()

#-----------------------------intro screen---------------------------------
spaceship_title = pygame.transform.rotozoom(player.sprite.image,30,2)
spaceship_title_rect = spaceship_title.get_rect(center = (640,300))
title_surf = titlefont.render('Spaceship Game',True,'Gray')
title_rect = title_surf.get_rect(center = (640,100))
instruction_surf = mainfont.render('Press R to start',True,'Gray')
instruction_rect = instruction_surf.get_rect(center = (640,500))

#-------------------------------Timer---------------------------------------
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

#meteor shower
meteor_shower = pygame.USEREVENT + 2
pygame.time.set_timer(meteor_shower,40000)
meteor_start = 0
meteor_shower_surf = titlefont.render('METEOR SHOWER',True,'#ff4576')
meteor_shower_rect = meteor_shower_surf.get_rect(center=(640,300))


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
                        print('hihihi')
                        obstacles.add(Obstacle('comet'))
                        obstacles.add(Obstacle('comet'))
                else:
                    meteor_shower_on = False
            else:
                if event.type == obstacle_timer:
                    obstacles.add(Obstacle(choice(['comet','asteroid','asteroid','asteroid'])))
                if event.type == meteor_shower:
                    meteor_start = pygame.time.get_ticks()
                    meteor_shower_on = True

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_active = True
                start_time = pygame.time.get_ticks()


    #actual game
    if game_active:
        game_time_index+=0.001
        #----------------------background---------------------------
        if bg_index <=1280: screen.blit(bg1,(-bg_index, 0))
        else: screen.blit(bg1,(2560-bg_index,0))
        screen.blit(bg2, (1280 - bg_index, 0))
        bg_index += 1+int(game_time_index)
        bg_index = bg_index%2560

        if meteor_shower_on and pygame.time.get_ticks()-meteor_start < 2000:
            screen.blit(meteor_shower_surf, meteor_shower_rect)
        #player and obstacles
        player.draw(screen)
        player.update()

        obstacles.draw(screen)
        obstacles.update()

        score = display_score()

        game_active = collisions()

    #----------------------------home screen-------------------------------------
    else:
        #background
        if bg_index <=1280: screen.blit(bg1,(-bg_index, 0))
        else: screen.blit(bg1,(2560-bg_index,0))
        screen.blit(bg2, (1280 - bg_index, 0))
        bg_index += 1
        bg_index = bg_index%2560

        screen.blit(spaceship_title,spaceship_title_rect)
        screen.blit(title_surf,title_rect)

        game_time_index=0
        player.sprite.gravity = 0
        player.sprite.rect.midleft = (200, 400)

        #-----------------------score--------------------------------------------
        if score == 0:
            if highscore > 0:
                highscore_message = mainfont.render(f'Highscore: {highscore}', True, 'Gray')
                highscore_rect = highscore_message.get_rect(center=(640, 650))
                screen.blit(highscore_message,highscore_rect)
            screen.blit(instruction_surf,instruction_rect)
        else:
            if score > highscore:
                highscore = score
                f = open('savedata.py','w')
                f.write('highscore = '+str(highscore)+'\n')
                f.close()
            score_message = mainfont.render(f'Your score: {score}', True, 'Gray')
            score_rect = score_message.get_rect(center=(640, 600))
            highscore_message = mainfont.render(f'Highscore: {highscore}',True,'Gray')
            highscore_rect = highscore_message.get_rect(center = (640,650))
            screen.blit(instruction_surf,instruction_rect)
            screen.blit(score_message, score_rect)
            screen.blit(highscore_message,highscore_rect)




    pygame.display.update()
    clock.tick(60)