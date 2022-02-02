import math
import random
import pygame
from pygame import mixer

pygame.init()

# set width and height of game window
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background
background_img = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0,736))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# Bullet
# Ready = you can't see the bullet
# Fire = bullet is being fired

bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = -5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
text_x = 10
text_y = 10

# Score
over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    # Create score image and then draw it on the screen
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (300, 270))

def player(x,y):
    screen.blit(player_img,(x, y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x, y))

def fire_bullet(x,y):
    screen.blit(bullet_img,(x+16,y+10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(bullet_x + 16 - enemy_x,2)
                         + math.pow(bullet_y + 16 - enemy_y,2))
    if distance < 27:
        return True
    else:
        return False

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
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_state = "fire"
                    bullet_x = player_x

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736

    # Enemy movement
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] < 0:
            enemy_x_change[i] = 3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] > 736:
            enemy_x_change[i] = -3
            enemy_y[i] += enemy_y_change[i]

        # Game over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000 # shift invaders off bottom of screen
            game_over_text()
            break

    # Bullet movement
    if bullet_y < 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y += bullet_y_change

    for i in range(num_of_enemies):
        collision = is_collision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)

    player(player_x,player_y)
    show_score(text_x, text_y)
    pygame.display.update()