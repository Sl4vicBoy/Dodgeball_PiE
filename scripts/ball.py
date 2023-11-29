import pygame
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT
import math
from random import randint


class Ball(pygame.sprite.Sprite):
    COLOR = 'Black'
    RADIUS = 10

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x_vel = randint(3, 5)
        self.y_vel = randint(0, 5)
        self.image = pygame.Surface((Ball.RADIUS * 2, Ball.RADIUS * 2))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        pygame.draw.circle(screen, Ball.COLOR, self.rect.center, Ball.RADIUS)

    def move(self):  # how we move the ball, always plus vel can be positive or negative
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def check_collision_wall(self, walls):
        if self.y + self.radius > SCREEN_HEIGHT or self.y - self.radius < 0:
            self.y_vel *= -1
        if self.x + self.radius > SCREEN_WIDTH or self.x-self.radius < 0:
            self.x_vel *= -1

    # def handle_collision_player(self, player):
    #     distance = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
    #     if distance < self.radius + player.radius:
    #         # Collision occurred
    #         # You can implement your collision handling logic here
    #         # For example, change the direction of the ball
    #         self.x_vel *= 0
    #         self.y_vel *= 0
    #         # ball.x = SCREEN_WIDTH//2
    #         # ball.y = SCREEN_HEIGHT//2
