import pygame
import random

pygame.init()

# set width and height of game window
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background
background_img = pygame.image.load('background.png')

# Player
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0

# Enemy
enemy_img = pygame.image.load('enemy.png')
enemy_x = random.randint(0,736)
enemy_y = random.randint(50,150)
enemy_x_change = 4
enemy_y_change = 40

# Bullet
# Ready = you can't see the bullet
# Fire = bullet is being fired

bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = -5
bullet_state = "ready"

def player(x,y):
    screen.blit(player_img,(x, y))

def enemy(x,y):
    screen.blit(enemy_img,(x, y))

def fire_bullet(x,y):
    screen.blit(bullet_img,(x+16,y+10))

# Game loop
running = True
while running:
    # Set backgound colour using RGB code
    #screen.fill((0, 0, 30))
    screen.blit(background_img,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed, check whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -2
            elif event.key == pygame.K_RIGHT:
                player_x_change = 2
            elif event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_state = "fire"
                    bullet_x = player_x

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736

    enemy_x += enemy_x_change
    if enemy_x < 0:
        enemy_x_change = 3
        enemy_y += enemy_y_change
    elif enemy_x > 736:
        enemy_x_change = -3
        enemy_y += enemy_y_change

    # Bullet movement
    if bullet_y < 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y += bullet_y_change

    player(player_x,player_y)
    enemy(enemy_x,enemy_y)
    pygame.display.update()