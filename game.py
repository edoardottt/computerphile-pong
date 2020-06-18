#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://github.com/edoardottt
https://edoardoottavianelli.it
"""

#=============IMPORT=============
import pygame
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

#=============PREPARATION============

squashpong = '''
                           _                             
 ___  __ _ _   _  __ _ ___| |__  _ __   ___  _ __   __ _ 
/ __|/ _` | | | |/ _` / __| '_ \| '_ \ / _ \| '_ \ / _` |
\__ \ (_| | |_| | (_| \__ \ | | | |_) | (_) | | | | (_| |
|___/\__, |\__,_|\__,_|___/_| |_| .__/ \___/|_| |_|\__, |
        |_|                     |_|                |___/ 
'''
pygame.init()
print("https://github.com/edoardottt/squashpong")
print("https://edoardoottavianelli.it")
print(squashpong)

WIDTH = 1200
HEIGHT = 600
BORDER = 20
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GREEN = pygame.Color("green")
BLUE = pygame.Color("blue")
RED = pygame.Color("red")
bgColor = BLACK
ball_color = RED
VELOCITY = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#-------Ball-------
class Ball:
    
    RADIUS = 15
    
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
    def show(self,color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.RADIUS)
        
    def update(self, paddle_y, paddle_WIDTH, paddle_HEIGHT):
        newx = self.x + self.vx
        newy = self.y + self.vy
        
        if paddle_y - paddle_HEIGHT//2 <= newy + self.RADIUS and newy - self.RADIUS <= paddle_y + paddle_HEIGHT//2 \
            and newx + self.RADIUS >= WIDTH - paddle_WIDTH:
            self.vx = - self.vx
        
        if newx < BORDER + self.RADIUS:
            self.vx = - self.vx
        elif newy < BORDER + self.RADIUS or newy > HEIGHT - BORDER - self.RADIUS:
            self.vy = - self.vy
        self.show(bgColor)
        self.x += self.vx
        self.y += self.vy
        self.show(ball_color)
        
#-------Paddle-------
class Paddle:
    WIDTH = 20
    HEIGHT = 100
    
    def __init__(self,y):
        self.y = y
        
    def show(self, colour):
        pygame.draw.rect(screen, colour, pygame.Rect(WIDTH - self.WIDTH, self.y - self.HEIGHT//2,self.WIDTH,self.HEIGHT))
        
    def update(self,mouse):
        #mouse = pygame.mouse.get_pos()[1]
        if not(mouse - self.HEIGHT//2 <= BORDER or mouse + self.HEIGHT//2 >= HEIGHT - BORDER):
            self.show(bgColor)
            self.y = mouse
            self.show(BLUE)
        elif mouse + self.HEIGHT//2 <= BORDER:
            self.y = self.HEIGHT//2 + BORDER
        else:
            self.y = HEIGHT -self.HEIGHT//2 - BORDER

paddle = Paddle(HEIGHT//2)
        
ball = Ball(WIDTH - Ball.RADIUS - paddle.WIDTH, HEIGHT//2, -VELOCITY, -VELOCITY)

#top border
pygame.draw.rect(screen, WHITE ,pygame.Rect((0,0),(WIDTH,BORDER)))

#left border
pygame.draw.rect(screen, WHITE ,pygame.Rect(0,0,BORDER,HEIGHT))

#bottom border
pygame.draw.rect(screen, WHITE ,pygame.Rect(0,HEIGHT - BORDER,WIDTH,BORDER))

ball.show(ball_color)

paddle.show(BLUE)

sample = open("game.csv","a")
#print("x,y,vx,vx,Paddle.y", file=sample)

pong = pd.read_csv("game.csv")
pong = pong.drop_duplicates()

x = pong.drop(columns="Paddle.y")
y = pong["Paddle.y"]

clf = KNeighborsRegressor(n_neighbors=3)

clf.fit(x,y)

df = pd.DataFrame(columns=['x','y','vx','vy'])

#=============GAME============
while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT: break

    toPredict = df.append({'x':ball.x, 'y':ball.y, 'vx': ball.vx, 'vy':ball.vy}, ignore_index=True)
    shouldMove = clf.predict(toPredict)
    
    ball.update(paddle.y, paddle.WIDTH, paddle.HEIGHT)
    
    paddle.update(int(shouldMove))
    
    #refresh
    pygame.display.flip()
    
    #collecting data
    print("{},{},{},{},{}".format(ball.x,ball.y,ball.vx,ball.vy,paddle.y), file=sample)

pygame.quit()