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

banner = '''
'''
pygame.init()
print("https://github.com/edoardottt/computerphile-pong")
print("https://edoardoottavianelli.it")
print(banner)

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
FRAMERATE = 60

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
            and (newx + self.RADIUS >= WIDTH - paddle_WIDTH or newx - self.RADIUS <= Paddle.WIDTH):
            self.vx = - self.vx
            
        if newy < BORDER + self.RADIUS or newy > HEIGHT - BORDER - self.RADIUS:
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
        
    def show(self, colour,x):
        pygame.draw.rect(screen, colour, pygame.Rect(x, self.y - self.HEIGHT//2,self.WIDTH,self.HEIGHT))
        
    def update(self,mouse,x):
        if not(mouse - self.HEIGHT//2 <= BORDER or mouse + self.HEIGHT//2 >= HEIGHT - BORDER):
            self.show(bgColor,x)
            self.y = mouse
            self.show(BLUE,x)
        elif mouse + self.HEIGHT//2 <= BORDER:
            self.y = self.HEIGHT//2 + BORDER
        else:
            self.y = HEIGHT -self.HEIGHT//2 - BORDER

paddle = Paddle(HEIGHT//2)

user_paddle = Paddle(HEIGHT//2)
        
ball = Ball(WIDTH - Ball.RADIUS - paddle.WIDTH, HEIGHT//2, -VELOCITY, -VELOCITY)

#top border
pygame.draw.rect(screen, WHITE ,pygame.Rect((0,0),(WIDTH,BORDER)))

#bottom border
pygame.draw.rect(screen, WHITE ,pygame.Rect(0,HEIGHT - BORDER,WIDTH,BORDER))

ball.show(ball_color)

paddle.show(BLUE,WIDTH - Paddle.WIDTH)

user_paddle.show(BLUE, WIDTH - Paddle.WIDTH)

#sample = open("game.csv","a")
#print("x,y,vx,vx,Paddle.y", file=sample)

pong = pd.read_csv("game.csv")
pong = pong.drop_duplicates()

x = pong.drop(columns="Paddle.y")
y = pong["Paddle.y"]

clf = KNeighborsRegressor(n_neighbors=3)

clf.fit(x,y)

df = pd.DataFrame(columns=['x','y','vx','vy'])

clock = pygame.time.Clock()

#=============GAME============
while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT: break

    toPredict = df.append({'x':ball.x, 'y':ball.y, 'vx': ball.vx, 'vy':ball.vy}, ignore_index=True)
    shouldMove = clf.predict(toPredict)
    
    paddle.update(int(shouldMove),WIDTH - Paddle.WIDTH)
    
    ball.update(paddle.y, paddle.WIDTH, paddle.HEIGHT)
    
    user_paddle.update(pygame.mouse.get_pos()[1],0)
    
    ball.update(user_paddle.y, user_paddle.WIDTH, user_paddle.HEIGHT)
    
    clock.tick(FRAMERATE)
    
    #refresh
    pygame.display.flip()
    
    #collecting data
    #print("{},{},{},{},{}".format(ball.x,ball.y,ball.vx,ball.vy,paddle.y), file=sample)

pygame.quit()