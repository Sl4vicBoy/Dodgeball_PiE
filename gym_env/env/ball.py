import pygame
import os
import math
from env.constant_values import FPS, LEFT, RIGHT, NONE
import numpy as np

class Ball(pygame.sprite.Sprite):
    DIAMETER = 20
    DECELERATION = 0.995

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.max_vel = None
        ball_img = pygame.image.load(os.path.join('env', 'Assets', 'balls', 'basket-ball.png')).convert_alpha()
        ball_img_scaled = pygame.transform.scale(ball_img, (self.DIAMETER, self.DIAMETER))
        self.image = ball_img_scaled
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.vel = pygame.math.Vector2
        self.dvel = pygame.math.Vector2
        self.danger = NONE
        self.caught_by_player = None

    def def_vel(self, x_vel, y_vel):
        self.vel = pygame.math.Vector2(x_vel, y_vel)
        self.max_vel = pygame.math.Vector2(x_vel, y_vel)
        self.dvel = pygame.math.Vector2(self.vel.x / (FPS ** 2), self.vel.y / (FPS ** 2))

    def maintain_collision_obstacle(self, obstacles, players_playing):
        collision = pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask)
        if collision:
            obstacle = collision[0]
            if obstacle.destroyable:
                if not obstacle.bomb:
                    obstacle.update(self.vel, self.max_vel)
                elif obstacle.bomb:
                    obstacle.update(self.vel, self.max_vel, players_playing)
            if (self.rect.bottom <= obstacle.rect.bottom + self.DIAMETER and
                    self.rect.top >= obstacle.rect.top - self.DIAMETER):
                if self.rect.right <= obstacle.rect.left:
                    self.rect.center -= (2 * self.dvel.x, 0)
                    self.vel.x *= -1
                elif self.rect.left >= obstacle.rect.right:
                    self.rect.x += 2 * self.dvel.x
                    self.vel.x *= -1
                self.vel.x *= -1
            if self.rect.x in range(obstacle.rect.left - 1, obstacle.rect.right + 1):
                if self.rect.y >= obstacle.rect.centery:
                    self.rect.y += self.dvel.y
                elif self.rect.y <= obstacle.rect.centery:
                    self.rect.y -= self.dvel.y
                self.vel.y *= -1
                self.vel.x *= -1

    def check_collision_player(self, players_playing):
        collision = None
        if self.caught_by_player is None:
            collision = pygame.sprite.spritecollide(self, players_playing, False, pygame.sprite.collide_mask)
        if collision:
            player = collision[0]
            if self.danger == player.team:
                player.bench = True
        return collision

    def move(self):
        if self.caught_by_player:
            player_width = self.caught_by_player.image.get_width()
            ball_width = self.image.get_width()
            self.rect.centery = self.caught_by_player.rect.centery
            if self.caught_by_player.team == RIGHT:
                self.rect.centerx = self.caught_by_player.rect.centerx - player_width / 2 - ball_width
            else:
                self.rect.centerx = self.caught_by_player.rect.centerx + player_width / 2 + ball_width
        else:
            self.vel *= self.DECELERATION
            self.rect.center += self.vel
            speed = pygame.math.Vector2.length(self.vel)
            if speed < 2:
                self.danger = NONE

    def throw_a_ball(self, angle):
        throwing_angle = angle
        if self.caught_by_player.team == LEFT:
            self.danger = RIGHT
        if self.caught_by_player.team == RIGHT:
            self.danger = LEFT
            throwing_angle = np.radians(180) - angle

        throwing_x_vel = np.cos(throwing_angle) * 5
        throwing_y_vel = np.sin(throwing_angle) * 5
        self.def_vel(throwing_x_vel, throwing_y_vel)
        self.caught_by_player = None



