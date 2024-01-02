import pygame
import os
from constant_values import BORDER_COLOR
from hpbar import HpBar


class Obstacle(pygame.sprite.Sprite):  
    def __init__(self, width, height, x, y,  color=BORDER_COLOR, destroyable=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.bomb = False

        self.collision_ball = True
        self.destroyable = destroyable

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    @staticmethod
    def get_impact_power(ball_velocity, max_ball_velocity):
        vel_length = ball_velocity.length()
        max_vel_length = max_ball_velocity.length()
        impact_power  = vel_length/ max_vel_length 
        return impact_power

class Midline(Obstacle):
    def __init__(self, width, height, x, y, color='violet'):
        super().__init__(width, height, x, y, color)
        self.collision_ball = False
        

class HpObstacle(Obstacle):
    def __init__(self, width, height, x, y, color='blue', destroyable=True, max_health = 4):
        super().__init__(width, height, x, y, color, destroyable)
        self.max_health = max_health
        self.current_health = max_health
        self.hp_bar = HpBar(max_health, self.rect)
        self.bomb = False

    def draw(self, screen):
        super().draw(screen)
        self.hp_bar.draw(screen)

    def update(self,ball_velocity, max_ball_velocity):
        self.current_health -= super().get_impact_power(ball_velocity,max_ball_velocity)*(self.max_health /2)
        if self.current_health > 0:
            self.hp_bar.hp_bar_update(self.current_health)
        else:
            self.kill()

class BombObstacle(Obstacle):
    def __init__(self, width, height, x, y, color = 'crimson', destroyable=True, max_velocity_rate = 0.7, bomb_radius =  250):
        super().__init__(width, height, x, y, color, destroyable)
        self.max_velocity_rate = max_velocity_rate
        self.bomb = True
        self.bomb_radius = bomb_radius
        self.bomb_x_range = (x - self.bomb_radius, x + self.bomb_radius)
        self.bomb_y_range = (y - self.bomb_radius, y + self.bomb_radius)

    def draw(self, screen):
        super().draw(screen)
    
    def update(self,ball_velocity, max_ball_velocity, players_playing):
        velocity_rate = super().get_impact_power(ball_velocity, max_ball_velocity)
        if velocity_rate > self.max_velocity_rate :
            for player in players_playing:
                if player.rect.x in range(self.bomb_x_range[0],self.bomb_x_range[1]) and player.rect.y in range(self.bomb_y_range[0], self.bomb_y_range[1]):
                    player.bench = True
                 
            self.kill()
        
         

    
    




