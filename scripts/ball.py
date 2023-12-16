import pygame,os
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from random import uniform
from player import Player


class Ball(pygame.sprite.Sprite):
    DIAMETER = 20
    DECELERATION=1

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        ball_img = pygame.image.load(os.path.join('Assets', 'balls', 'basket-ball.png')).convert_alpha()
        ball_img_scaled = pygame.transform.scale(ball_img, (self.DIAMETER, self.DIAMETER))
        self.image = ball_img_scaled
        self.rect = self.image.get_rect(center=(x, y)) 
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image= self.mask.to_surface()
        self.vel = pygame.math.Vector2 #Vector2 == dx,dy - o ile sie porusza co klatke
        self.speed=3
        self.dvel = pygame.math.Vector2
        self.danger=1
        self.caught_by_player=None

    def def_rand_vel(self,x_vel,y_vel):
        self.vel = pygame.math.Vector2(x_vel, y_vel)
        self.dvel = pygame.math.Vector2(self.vel.x / (FPS ** 2), self.vel.y / (FPS ** 2))

    def maintain_collision_obstacle(self, obstacles):
        collision = pygame.sprite.spritecollide(self, obstacles, False)
        
        for obstacle in collision:
            if (self.rect.bottom <= obstacle.rect.bottom + self.DIAMETER and
                    self.rect.top >= obstacle.rect.top - self.DIAMETER):
                    if self.rect.right <= obstacle.rect.left:
                        self.rect.center -= (2 * self.dvel.x, 0)
                        self.vel.x *= -1
                    elif self.rect.left >= obstacle.rect.right:
                        self.rect.x += 2 * self.dvel.x
                        self.vel.x *= -1
                    self.vel.x *= -1
            if self.rect.x in range(obstacle.rect.left-1, obstacle.rect.right + 1):
                if self.rect.y >= obstacle.rect.centery:
                    self.rect.y += self.dvel.y
                elif self.rect.y <= obstacle.rect.centery:
                    self.rect.y -= self.dvel.y
                self.vel.y *= -1
                self.vel.x *= -1

    def check_collision_player(self, players_playing):
        collision = pygame.sprite.spritecollide(self, players_playing, False)
        if collision:
            player = collision[0]
            if player.catch_ball(self):
                pass
            else:
                player.bench = True
        return collision#return a list containing all players_playing colliding with self

    def move(self):
        if self.caught_by_player:
            self.rect.center = self.caught_by_player.rect.center#follow the players that caught you
        else:    
            self.vel*=self.DECELERATION
            self.rect.center += self.vel
            self.speed =pygame.math.Vector2.length(self.vel)
            if self.speed<3:
                self.danger=0
            else:
                self.danger=1
    
               
