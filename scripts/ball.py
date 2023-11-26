import pygame
from constant_values import BLACK,SCREEN_WIDTH, SCREEN_HEIGHT
import math
from random import randint

class Ball:
    MAX_VEL = 5
    COLOR = BLACK
    #RADIUS_BALL = 10
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = randint(3, 5)
        # when the programme starts, the ball moves horizontally
        #this x velocity will never change
        self.y_vel =randint(0,5)

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.radius)

    def move(self):#how we move the ball, always plus vel can be positive or negative
        self.x += self.x_vel
        self.y += self.y_vel

    def handle_collision_wall(self):
        if self.y + self.radius > SCREEN_HEIGHT or self.y - self.radius < 0:
            self.y_vel *= -1
        if self.x + self.radius > SCREEN_WIDTH or self.x-self.radius < 0:
            self.x_vel *= -1

    def handle_collision_player(self, player):
        distance = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
        if distance < self.radius + player.radius:
            # Collision occurred
            # You can implement your collision handling logic here
            # For example, change the direction of the ball
            self.x_vel *= 0
            self.y_vel *= 0
            #ball.x = SCREEN_WIDTH//2
            #ball.y = SCREEN_HEIGHT//2
