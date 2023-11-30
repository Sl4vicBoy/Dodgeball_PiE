import pygame
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT
import math
from random import randint


class Ball(pygame.sprite.Sprite):
    COLOR = 'Black'
    RADIUS = 10

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.vel = pygame.Vector2(randint(3, 5), randint(0, 5))
        self.image = pygame.Surface((Ball.RADIUS * 2, Ball.RADIUS * 2))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        pygame.draw.circle(screen, Ball.COLOR, self.rect.center, Ball.RADIUS)

    def move(self):  # how we move the ball, always plus vel can be positive or negative
        self.rect.center += self.vel

    def check_collision_wall(self):
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.vel.y *= -1
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.vel.x *= -1

    def check_collision_player(self, all_players):
        player = pygame.sprite.spritecollideany(self, all_players)
        if player:
            self.vel.xy = (0, 0)
    
    def check_collission_obstacle(self,obstacles):
        pass
