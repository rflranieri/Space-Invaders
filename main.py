import math
import random
import pygame
from pygame import mixer

# Inicializa o pygame
pygame.init()

# Tela
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Som de fundo
mixer.music.load('background.wav')
mixer.music.set_volume(0.1)
mixer.music.play(-1)

# Título e Ícone
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Jogador
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Inimigos
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

def spawn_enemies(num):
    for _ in range(num):
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(0.9)
        enemyY_change.append(40)

spawn_enemies(num_of_enemies)

# Balas
bulletImg = pygame.image.load('bullet.png')
bullets = []  # Lista de balas

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Game States
game_state = 'start'  # start, playing, game_over


# Funções

def show_start_screen():
    title = over_font.render("SPACE INVADERS", True, (255, 255, 255))
    press = font.render("Pressione ENTER para começar", True, (255, 255, 255))
    screen.blit(title, (150, 250))
    screen.blit(press, (220, 320))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    press = font.render("Pressione ENTER para reiniciar", True, (255, 255, 255))
    screen.blit(press, (230, 320))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    bullets.append({'x': x + 16, 'y': y + 10})


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27


# Loop Principal
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == 'playing':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -3
                if event.key == pygame.K_RIGHT:
                    playerX_change = 3
                if event.key == pygame.K_SPACE:
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.set_volume(0.2)
                    bullet_Sound.play()
                    fire_bullet(playerX, playerY)

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    playerX_change = 0

        elif game_state in ('start', 'game_over'):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Resetar jogo
                    playerX = 370
                    playerX_change = 0
                    bullets = []
                    enemyImg = []
                    enemyX = []
                    enemyY = []
                    enemyX_change = []
                    enemyY_change = []
                    spawn_enemies(num_of_enemies)
                    score_value = 0
                    game_state = 'playing'

    if game_state == 'start':
        show_start_screen()

    elif game_state == 'playing':
        # Jogador
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Inimigos
        for i in range(len(enemyX)):
            if enemyY[i] > 440:
                game_state = 'game_over'
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.9
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.9
                enemyY[i] += enemyY_change[i]

            # Verificar colisões com balas
            for bullet in bullets:
                collision = is_collision(enemyX[i], enemyY[i], bullet['x'], bullet['y'])
                if collision:
                    explosion_Sound = mixer.Sound('explosion.wav')
                    explosion_Sound.set_volume(0.3)
                    explosion_Sound.play()
                    try:
                        bullets.remove(bullet)
                    except:
                        pass
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                    score_value += 1

                    # Aumentar dificuldade
                    if score_value % 10 == 0:
                        spawn_enemies(1)  # Adiciona mais 1 inimigo

            enemy(enemyX[i], enemyY[i], i)

        # Movimento das balas
        for bullet in bullets[:]:
            bullet['y'] -= 10
            screen.blit(bulletImg, (bullet['x'], bullet['y']))
            if bullet['y'] <= 0:
                bullets.remove(bullet)

        player(playerX, playerY)
        show_score(textX, textY)

    elif game_state == 'game_over':
        game_over_text()
        show_score(textX, textY)

    pygame.display.update()
