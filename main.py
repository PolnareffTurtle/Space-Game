import pygame
from sys import exit
from random import randint, choice
from savedata import *

pygame.init()
screen = pygame.display.set_mode((1280,720))
spaceship = pygame.transform.rotozoom(pygame.image.load('graphics/spaceship.png').convert_alpha(),0,0.5)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship
        self.rect = self.image.get_rect(midleft = (200,400))
        self.gravity = 0
        self.falling = True

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity += -0.6
        else:
            self.gravity += 0.5

    def apply_gravity(self):
        #max and min for gravity
        if self.gravity > 10: self.gravity = 10
        if self.gravity < -10: self.gravity = -10
        self.rect.y += self.gravity
        #max and min for position
        if self.rect.top < 20: self.rect.top,self.gravity = 20,0
        if self.rect.bottom > 700: self.rect.bottom,self.gravity = 700,0
        self.image = pygame.transform.rotozoom(spaceship,-self.gravity,1)

    def update(self):
        self.player_input()
        self.apply_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self): #TODO: create different types for the obstacles --> def __init__(self,type)
        super().__init__()
        self.image = pygame.image.load('graphics/asteroid.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,0.4)
        self.rect = self.image.get_rect(midleft = (randint(1300,1500),randint(20,700)))

    def destroy(self):
        if self.rect.right < 0:
            self.kill()
    def update(self):
        self.rect.x += -4
        self.destroy()

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 100
    score_surf = mainfont.render(f'Score: {current_time}', True, 'White')
    score_rect = score_surf.get_rect(topright = (1230,50))
    screen.blit(score_surf, score_rect)
    return current_time

def collisions():
    if pygame.sprite.spritecollide(player.sprite,obstacles,False):
        obstacles.empty()
        return False
    return True

#-------------------SAVE DATA----------------------

pygame.display.set_caption('Space Game')
clock = pygame.time.Clock()
mainfont = pygame.font.Font(None, 50)
titlefont = pygame.font.Font(None,100)
game_active = False
start_time = 0
score = 0

#background
bg_surf = pygame.image.load('graphics/background.png').convert()

#--------------------------GROUPS-------------------------------------
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()

#-----------------------------intro screen---------------------------------
spaceship_title = pygame.transform.rotozoom(player.sprite.image,30,2)
spaceship_title_rect = spaceship_title.get_rect(center = (640,400))
title_surf = titlefont.render('Spaceship Game',True,'Gray')
title_rect = title_surf.get_rect(center = (640,100))
instruction_surf = mainfont.render('Press Space to start',True,'Gray')
instruction_rect = instruction_surf.get_rect(center = (640,600))

#-------------------------------Timer---------------------------------------
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

#main loop
while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacles.add(Obstacle())
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()


    #actual game
    if game_active:
        screen.blit(bg_surf, (0, 0))
        falling = True
        score = display_score()

        player.draw(screen)
        player.update()

        obstacles.draw(screen)
        obstacles.update()

        game_active = collisions()

    #----------------------------home screen-------------------------------------
    else:
        screen.fill('#8662a1')
        screen.blit(spaceship_title,spaceship_title_rect)
        screen.blit(title_surf,title_rect)
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
                f.write('highscore = '+str(highscore))
                f.close()
            score_message = mainfont.render(f'Your score: {score}', True, 'Gray')
            score_rect = score_message.get_rect(center=(640, 600))
            highscore_message = mainfont.render(f'Highscore: {highscore}',True,'Gray')
            highscore_rect = highscore_message.get_rect(center = (640,650))
            screen.blit(score_message, score_rect)
            screen.blit(highscore_message,highscore_rect)




    pygame.display.update()
    clock.tick(60)