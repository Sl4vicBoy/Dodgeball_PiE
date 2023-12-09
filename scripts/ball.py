import pygame
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from random import randint


class Ball(pygame.sprite.Sprite):
    COLOR = 'Black'
    RADIUS = 10

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.vel = pygame.Vector2(randint(3, 5), randint(1, 5))
        self.image = pygame.Surface((Ball.RADIUS * 2, Ball.RADIUS * 2))
        self.rect = self.image.get_rect(center=(x, y))
        self.dvel = pygame.Vector2(self.vel.x/(FPS**2),self.vel.y/(FPS**2))

    def draw(self, screen):
        pygame.draw.circle(screen, Ball.COLOR, self.rect.center, Ball.RADIUS)

    def move(self):  # how we move the ball, always plus vel can be positive or negative
        self.rect.center += self.vel

    def check_collision_wall(self):
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.vel.y *= -1
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.vel.x *= -1

    def check_collision_player(self, players_playing):
        player = pygame.sprite.spritecollideany(self, players_playing)
        if player:
            # self.vel.xy = (0, 0)
            player.bench = True
    def check_collision_obstacle(self, obstacles):
        collision = pygame.sprite.spritecollide(self, obstacles, False)
        
        if collision:
            obstacle = collision[0]
            
                # Check left and right sides of the obstacle
            if self.rect.bottom <= obstacle.rect.bottom + 2*self.RADIUS and self.rect.top >= obstacle.rect.top - 2* self.RADIUS :

                    if self.rect.right <= obstacle.rect.left:
                        self.rect.center -= (2*self.dvel.x,0)
                        self.vel.x *= -1
                    elif self.rect.left >= obstacle.rect.right:
                         self.rect.x += 2*self.dvel.x
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
           








