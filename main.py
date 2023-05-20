import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()

bg_surf = pygame.image.load('graphics/underwater.jpeg').convert()

turtle_surf = pygame.image.load('graphics/turtle.png').convert_alpha()
turtle_rect = turtle_surf.get_rect(midleft=(200, 400))
player_gravity = 0

mainfont = pygame.font.Font(None, 50)
score_surf = mainfont.render('Score:', True, 'Black')
score_rect = score_surf.get_rect(topright = (1230,50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(bg_surf, (0, 0))
    screen.blit(score_surf, score_rect)
    falling = True

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
    turtle_rect.y += player_gravity

    # max and min y-value for turtle
    if turtle_rect.bottom > 700:
        turtle_rect.bottom = 700
        player_gravity = 0
    if turtle_rect.top < 20:
        turtle_rect.top = 20
        player_gravity = 0
    turtle_rect.y += player_gravity
    screen.blit(turtle_surf, turtle_rect)

    pygame.display.update()
    clock.tick(60)