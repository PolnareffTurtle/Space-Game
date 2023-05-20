import pygame
from sys import exit
from random import randint

#displays the score
def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 100
    score_surf = mainfont.render(f'Score: {current_time}', False, 'White')
    score_rect = score_surf.get_rect(topright = (1230,50))
    screen.blit(score_surf, score_rect)
    return current_time

#sets the asteroids moving across the screen
def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -= 5
            screen.blit(asteroid_surf,obstacle_rect)

        #remove obstacles that are too far left
        obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle.right > 0]

        return obstacle_rect_list
    else:
        return []

#runs through each obstacle and checks collision
def collisions(spaceship,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if obstacle_rect.colliderect(spaceship):
                return False
    return True

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Space Game')
clock = pygame.time.Clock()
mainfont = pygame.font.Font(None, 50)
titlefont = pygame.font.Font(None,100)
game_active = False
start_time = 0
score = 0

bg_surf = pygame.image.load('graphics/background.png').convert()

#spaceship
spaceship_surf = pygame.image.load('graphics/spaceship.png').convert_alpha()
spaceship_surf = pygame.transform.rotozoom(spaceship_surf,0,0.5)
spaceship_rect = spaceship_surf.get_rect(midleft=(200, 400))
player_gravity = 0

#obstacles
asteroid_surf = pygame.image.load('graphics/asteroid.png').convert_alpha()
asteroid_rect = asteroid_surf.get_rect(midleft = (1280,400))
obstacle_rect_list = []

#intro screen
spaceship_title = pygame.transform.rotozoom(spaceship_surf,30,2)
spaceship_title_rect = spaceship_title.get_rect(center = (640,400))
title_surf = titlefont.render('Spaceship Game',True,'Gray')
title_rect = title_surf.get_rect(center = (640,100))
instruction_surf = mainfont.render('Press Space to start',True,'Gray')
instruction_rect = instruction_surf.get_rect(center = (640,600))
score_surf = mainfont.render('High Score:',False,(64,64,64))

#Timer
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
            pass
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                asteroid_rect.left = 1280
                game_active = True
                start_time = pygame.time.get_ticks()
        if event.type == obstacle_timer:
            obstacle_rect_list.append(asteroid_surf.get_rect(center = (randint(1400,1600),randint(20,700))))

    #actual game
    if game_active:
        screen.blit(bg_surf, (0, 0))
        falling = True
        score = display_score()

        # gravity
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            falling = False
        if falling:
            player_gravity += 0.5
        else:
            player_gravity += -0.6
        if player_gravity > 10:
            player_gravity = 10
        if player_gravity < -10:
            player_gravity = -10
        spaceship_rect.y += player_gravity

        # max and min y-value for spaceship
        if spaceship_rect.bottom > 700:
            spaceship_rect.bottom = 700
            player_gravity = 0
        if spaceship_rect.top < 20:
            spaceship_rect.top = 20
            player_gravity = 0
        spaceship_rect.y += player_gravity
        spaceship_surf_rotated = pygame.transform.rotozoom(spaceship_surf,-player_gravity,1)
        screen.blit(spaceship_surf_rotated, spaceship_rect)

        # obstacles
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collisions(spaceship_rect,obstacle_rect_list)

    #home screen
    else:
        screen.fill('#8662a1')
        screen.blit(spaceship_title,spaceship_title_rect)
        screen.blit(title_surf,title_rect)
        obstacle_rect_list.clear()
        spaceship_rect.midleft = (200, 400)
        player_gravity = 0

        score_message = mainfont.render(f'Your score: {score}', False, 'Gray')
        score_message_rect = score_message.get_rect(center=(640, 600))

        if score == 0:
            screen.blit(instruction_surf,instruction_rect)
        else:
            screen.blit(score_message, score_message_rect)

        if score == 0:
            screen.blit(instruction_surf, instruction_rect)
        else:
            screen.blit(score_message, score_message_rect)


    pygame.display.update()
    clock.tick(60)