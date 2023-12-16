import pygame,os
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from random import uniform
from player import Player


class Ball(pygame.sprite.Sprite):
    DIAMETER = 20
    DECELERATION=0.992

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
        

    def move(self):
        self.vel*=self.DECELERATION
        self.rect.center += self.vel
        self.speed =pygame.math.Vector2.length(self.vel)
        if self.speed<3:
            self.danger=0
        else:
            self.danger=1    

    def check_collision_wall(self):
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.vel.y *= -1
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.vel.x *= -1

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

    def check_collision_player(self, players_playing):
        collision = pygame.sprite.spritecollide(self, players_playing, False)
        #return a list containing all players_playing colliding with self
        if collision:
            player = collision[0]
            if player.catch_ball(self):
                pass
            else:
                player.bench = True
        return collision

    def follow_caught_by_player(self):
        if self.caught_by_player:
            self.rect.center = self.caught_by_player.rect.center

    def move(self):#w ktory z dwoch sposobow pilka sie porusza, czy podaza za graczem czy normalnie sie odbija
        if not self.caught_by_player:
            self.vel*=self.DECELERATION
            self.rect.center += self.vel  
        else:
            self.follow_caught_by_player()
               
