import pygame
from sys import exit

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 100
    score_surf = mainfont.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(topright = (1230,50))
    screen.blit(score_surf, score_rect)
    return current_time

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
mainfont = pygame.font.Font(None, 50)
titlefont = pygame.font.Font(None,100)
game_active = True
start_time = 0

bg_surf = pygame.image.load('graphics/background.png').convert()

spaceship_surf = pygame.image.load('graphics/spaceship.png').convert_alpha()
spaceship_rect = spaceship_surf.get_rect(midleft=(200, 400))
player_gravity = 0


#score_surf = mainfont.render('Score:', True, 'Black')
# = score_surf.get_rect(topright = (1230,50))

#obstacles
asteroid_surf = pygame.image.load('graphics/asteroid.png').convert_alpha()
asteroid_rect = asteroid_surf.get_rect(midleft = (1280,400))

#intro screen
spaceship_title = pygame.transform.rotozoom(spaceship_surf,30,2)
spaceship_title_rect = spaceship_title.get_rect(center = (640,400))
title_surf = titlefont.render('Spaceship Game',True,'Gray')
title_rect = title_surf.get_rect(center = (640,100))
instruction_surf = mainfont.render('Press Space to start',True,'Gray')
instruction_rect = instruction_surf.get_rect(center = (640,600))
score_surf = mainfont.render('High Score:',False,(64,64,64))

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
        screen.blit(spaceship_surf, spaceship_rect)

        # obstacles
        asteroid_rect.x += -4
        if asteroid_rect.right < 0:
            asteroid_rect.left = 1280
        screen.blit(asteroid_surf, asteroid_rect)

        if asteroid_rect.colliderect(spaceship_rect):
            game_active = False

    else:
        screen.fill('Blue')
        screen.blit(spaceship_title,spaceship_title_rect)
        screen.blit(title_surf,title_rect)

        score_message = mainfont.render(f'Your score: {score}', False, (111, 196, 169))
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