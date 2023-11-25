import pygame
from constant_values import BLACK,SCREEN_WIDTH, SCREEN_HEIGHT
import math
from random import randint

class Ball:
    MAX_VEL = 5
    COLOR = BLACK
    #RADIUS_BALL = 10
    def __init__(self,x,y,radius):
        self.x=x
        self.y=y
        self.radius = radius
        self.x_vel = randint(3,5)
        # when the programme starts, the ball moves horizontally
        #this x velocity will never change
        self.y_vel =randint(0,5)    

    def draw(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.radius) 

    def move(self):#how we move the ball, always plus vel can be positive or negative
        self.x +=self.x_vel   
        self.y+=self.y_vel   

def handle_collision_wall(ball):
    #start with the ceiling
    if ball.y + ball.radius >= SCREEN_HEIGHT:#if we dont add radius, we've got just the centre of the ball
        ball.y_vel *= -1  #zmieniamy kierunek przemieszczenia yekowego
    elif ball.y-ball.radius <= 0:
        ball.y_vel *= -1            
     #start with the ceiling
    elif ball.x +ball.radius >= SCREEN_WIDTH:#if we dont add radius, we've got just the centre of the ball
        ball.x_vel *= -1  #zmieniamy kierunek przemieszczenia yekowego
    elif ball.x-ball.radius <= 0:
        ball.x_vel *= -1 

def handle_collision_players(ball,obstacle):
    #collitions with obstacles
    distance = math.sqrt((ball.x - obstacle.x)**2 + (ball.y - obstacle.y)**2)
    if distance < ball.radius + obstacle.radius:
        # Collision occurred
        # You can implement your collision handling logic here
        # For example, change the direction of the ball
        ball.x_vel *= 0
        ball.y_vel *= 0
        #ball.x = SCREEN_WIDTH//2
        #ball.y = SCREEN_HEIGHT//2
