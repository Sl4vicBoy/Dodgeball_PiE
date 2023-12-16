import pygame,os
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from random import uniform
from player import Player


class Ball(pygame.sprite.Sprite):
    DIAMETER = 20
    DECELERATION=0.999

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        ball_img = pygame.image.load(os.path.join('Assets', 'balls', 'basket-ball.png')).convert_alpha()
        ball_img_scaled = pygame.transform.scale(ball_img, (self.DIAMETER, self.DIAMETER))
        self.image = ball_img_scaled #nasz obrazek - pilka
        self.rect = self.image.get_rect(center=(x, y)) #mozna pilke ustawic gdzie sie chce
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image= self.mask.to_surface()#draws a mask
        self.vel = pygame.math.Vector2 #Vector2 == dx,dy - o ile sie porusza co klatke
        self.dvel = pygame.math.Vector2
        self.caught_player=None

    def def_rand_vel(self):
        self.vel = pygame.math.Vector2(uniform(4, 6), uniform(4, 6))
        self.dvel = pygame.math.Vector2(self.vel.x / (FPS ** 2), self.vel.y / (FPS ** 2))

    def move(self):  # how we move the ball, always plus vel can be positive or negative
        self.vel*=self.DECELERATION
        self.rect.center += self.vel#zwieksza sie caly czas o ten sam wektor w kazdej klatce, czyli

    def check_collision_wall(self):
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.vel.y *= -1
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.vel.x *= -1

    def check_collision_player(self, players_playing):
        collision = pygame.sprite.spritecollide(self, players_playing, False)
        if collision:
            player = collision[0]
            # self.vel.xy = (0, 0)
            player.bench = True
        return collision

    def check_collision_obstacle(self, obstacles):
        collision = pygame.sprite.spritecollide(self, obstacles, False)
        
        if collision:
            obstacle = collision[0]
            # Check left and right sides of the obstacle
            if (self.rect.bottom <= obstacle.rect.bottom + self.DIAMETER and
                    self.rect.top >= obstacle.rect.top - self.DIAMETER):

                if self.rect.right <= obstacle.rect.left:
                    self.rect.center -= (2 * self.dvel.x, 0)
                    self.vel.x *= -1
                elif self.rect.left >= obstacle.rect.right:
                    self.rect.x += 2 * self.dvel.x
                    self.vel.x *= -1
                self.vel.x *= -1

            if self.rect.x in range(obstacle.rect.left, obstacle.rect.right + 1):
                # Check top and bottom sides of the obstacle
                if self.rect.y >= obstacle.rect.centery:
                    self.rect.y += self.dvel.y
                    self.vel.y *= -1
                elif self.rect.y <= obstacle.rect.centery:
                    self.rect.y -= self.dvel.y
                    self.vel.y *= -1

    def set_caught_player(self, player):
        self.caught_player = player

    def follow_caught_player(self):
        if self.caught_player:
            self.rect.center = self.caught_player.rect.center

    def move(self):
        if not self.caught_player:
            self.rect.center += self.vel
            self.vel*=self.DECELERATION
            # Your existing move logic here
        else:
            # Follow the caught player
            self.follow_caught_player()
               
