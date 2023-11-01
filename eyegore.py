import pygame, sys, random
from pygame.locals import *
import time as t
import math
import random
import os, sys

pygame.init()
pygame.mixer.init(44100, -16, 2, 512)
win = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('eyegore')
char = pygame.image.load('folderimages\\eyegore.png')
char_hurt = pygame.image.load('folderimages\\eyegore_hurt.png')
walkLeft = pygame.image.load('folderimages\\walkleft.png')
walkRight = pygame.image.load('folderimages\\walkright.png')
image = pygame.image.load('folderimages\\level.png')
onionchar = pygame.image.load('folderimages\\onionleft1.png')
onionleft = pygame.image.load('folderimages\\onionleft1.png')
onionright = pygame.image.load('folderimages\\onionright1.png')
lives = 5
font = pygame.font.Font("freesansbold.ttf", 32)
testX = 10
testY = 10
jumpsfx = pygame.mixer.Sound('Audiofx/jumpsound.wav')
hurtfx = pygame.mixer.Sound('Audiofx/eyegorehurt.wav')


def show_lives(x, y):
    score = font.render("Lives : " + str(lives), True, (255, 255, 255))
    win.blit(score, (x, y))


def show_timer(x, y):
    stime = font.render("Time :" + str(counter), True, (255, 0, 0))
    win.blit(stime, (x, y))

count = "TIME"
counter, text = 600, ''.ljust(0)
pygame.time.set_timer(pygame.USEREVENT, 100)
font1 = pygame.font.Font('freesansbold.ttf', 32)
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.lives = 0
        self.hitbox = (self.x, self.y, 100, 170)
        self.image = pygame.image.load('folderimages\\eyegore.png')
        self.image2 = pygame.image.load('folderimages\\eyegore_hurt.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image2)

    def draw(self, win):
        if self.walkCount + 1 >= 5:
            self.walkCount = 0
        if self.left:
            win.blit(walkLeft, (self.x, self.y))
            self.walkCount += 0
        elif self.right:
            win.blit(walkRight, (self.x, self.y))
            self.walkCount += 0
        else:
            win.blit(char, (self.x, self.y))
            self.hitbox = (self.x + 110, self.y, self.width, self.height)
            pygame.draw.rect(win, (255, 255, 0), self.hitbox, 1)

    def hit(self):
        if man.hitbox[0] < enemy.x + 140 < man.hitbox[0] + man.hitbox[2] and \
                man.hitbox[1] < enemy.y + 140 < man.hitbox[1] + man.hitbox[3]:
            win.blit(self.image2, (man.x, man.y))
            global lives
            self.lives = lives
            lives -= 1
            #t.sleep(0.5)
            hurtfx.play()
            if man.lives <= 0:
                print('game over')


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, end):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 7
        self.end = end
        self.path = [self.end, self.x]
        self.left = False
        self.right = False
        self.walkCount = 0
        self.onionleft = onionleft
        self.onionright = onionright
        self.image = pygame.image.load('folderimages\\onionleft1.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        self.move()

        if self.walkCount + 1 >= 30:
            self.walkCount = 0
        elif self.left > 2:
            win.blit(self.onionleft[self.walkCount // 50], (self.x, self.y))
            self.walkCount += 1
        if self.right:
            win.blit(self.onionright[self.walkCount // 50], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(onionchar, (self.x, self.y))
            self.hitbox = (self.x + 170, self.y + 140, self.width, self.height + 60)
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0


def redrawGameWindow():
    win.blit(image, (0, 0))
    man.draw(win),
    man.hit(),
    show_lives(testX, testY),
    enemy.draw(win),
    x=400
    y=100
    show_timer(x, y)
    pygame.display.update()


# mainloop

man = Player(0, 360, 100, 160)
playergroup = pygame.sprite.Group()
playergroup.add(man)

enemy = Enemy(700, 221, 100, 100, 0)
enemygroup = pygame.sprite.Group()
enemygroup.add(enemy)
run1 = True

def intro():
    while run1:
        win1 = pygame.display.set_mode((1000, 1000))
        win1.fill((0, 0, 0))
        text_display = font.render("Eyegore use the space-bar to jump and arrow "
                                   "keys to move ", True, (255, 0, 255))
        x = 50
        y = 50
        win1.blit(text_display, (x, y))
        text_display1 = font.render("Click to Play", True, (255, 0, 255))
        win1.blit(text_display1, (400, 370))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    return pygame.display.update()


run2 = True
while run1 or run2:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if event.dict.get('caption') == 'Window 1':
                running1 = False
            elif event.dict.get('caption') == 'Window 2':
                running2 = False
    counter -=1
    text = str(counter) + str(count) if counter > 0 else "Level complete"
    clock.tick(60)
    if run1:
        # Update and render window 1
        intro()  # Fill with red color
        run1=False
        pygame.display.update()

    if run2:
        # Update and render window 2
        clock.tick(60)
        redrawGameWindow()# Fill with blue color


        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.x < 850 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
    else:
        man.right = False
        man.left = False
        man.walkCount = 5

    if not (man.isJump):
        if keys[pygame.K_SPACE]:
            man.isJump = True
            jumpsfx.play(0)
            man.right = False
            man.left = False
            man.walkCount = 5
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()





