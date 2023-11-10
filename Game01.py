import pygame
import math
import random
from pygame import mixer

#Initialization of Pygame
pygame.init()

#Creating the Screen
screen = pygame.display.set_mode((800,600))

#Creating the background
back = pygame.image.load("back.jpg")

#Creating the background sound
mixer.music.load("background.mp3")
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#player
ply_img = pygame.image.load("s1.png")
ply_X = 370
ply_Y = 480
plyX_change = 0
plyY_change = 0

#enemy
al_img = []
al_X = []
al_Y = []
alX_change = []
alY_change = []

num = 6

for i in range(num):
    al_img.append(pygame.image.load("alien.png"))
    al_X.append(random.randint(0,745))
    al_Y.append(random.randint(50, 150))
    alX_change.append(0.15)
    alY_change.append(40)

#bullet
#ready -> you can't fire bullet
#fire -> you can fire bullet
b_img = pygame.image.load("bullet.png")
b_X = 0
b_Y = 480
bX_change = 0
bY_change = 0.5
bstate = "ready"

#Scoreboard
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_X = 10
text_Y = 10

#Game Over
GO_font = pygame.font.Font("freesansbold.ttf", 64)

def player(x, y):
    screen.blit(ply_img, (x, y))

def alien(x, y, i):
    screen.blit(al_img[i], (x, y))

def bullet(x, y):
    global bstate
    bstate = "fire"
    screen.blit(b_img, (x + 16, y + 10))

def collision(alx, aly, bx, by):
    distance = math.sqrt( (math.pow( alx - bx , 2)) + (math.pow( aly - by, 2)) )
    if distance < 27:
        return True
    else:
        return False

def scoreboard(x, y):
    score_value = font.render("SCORE: " +str(score), True, (255,255,255))
    screen.blit(score_value, (x, y))

def game_over():
    go = GO_font.render("GAME OVER", True, (255,255,255))
    screen.blit(go, (200, 250))

running = True
while running:

    #RGB color for Background
    screen.fill((52, 52, 52))

    #Background Picture
    screen.blit(back,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #movement mechanism
        if event.type == pygame.KEYDOWN:
        #for movement of spaceship left and right
            if event.key == pygame.K_LEFT:
                plyX_change = -0.17
            if event.key == pygame.K_RIGHT:
                plyX_change = 0.17
        #for firing bullets
            if event.key == pygame.K_SPACE:
                if bstate is "ready" :
                    bs = mixer.Sound("laser.mp3")
                    bs.play()
                    b_X = ply_X
                    bullet(b_X, b_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                plyX_change = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                plyY_change = 0

    #Player Movement
    ply_X += plyX_change
    if ply_X <= 0:
        ply_X = 0
    elif ply_X >= 736:
        ply_X = 736

    #Enemy Movement
    for i in range(num):

        #Game Over
        if al_Y[i] > 425:
            for j in range(num):
                al_Y[j] = 2000
            game_over()
            break

        al_X[i] += alX_change[i]
        if al_X[i] <= 0:
            alX_change[i] = 0.15
            al_Y[i] += alY_change[i]
        elif al_X[i] >= 736:
            alX_change[i] = -0.15
            al_Y[i] += alY_change[i]

        #Collision detection
        col = collision(al_X[i], al_Y[i], b_X, b_Y)
        if col:
            cs = mixer.Sound("blast.mp3")
            cs.play()
            b_Y = 480
            bstate = "ready"
            score += 1
            print(score)
            al_X[i] = random.randint(0,735)
            al_Y[i] = random.randint(50, 150)

        alien(al_X[i], al_Y[i], i)

    #Bullet Movement
    if b_Y <= 0:
        b_Y = 480
        bstate = "ready"
    
    if bstate is "fire" :
        bullet(b_X, b_Y)
        b_Y -= bY_change

    player(ply_X, ply_Y)
    scoreboard(text_X, text_Y)

    pygame.display.update()