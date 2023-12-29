import pygame
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

        self.collision_ball = True
        self.destroyable = destroyable

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    @staticmethod
    def get_impact_power(ball_velocity, max_ball_velocity):
        vel_length = ball_velocity.length()
        max_vel_length = max_ball_velocity.length()
        impact_power  = vel_length/(2* max_vel_length)
        return impact_power

class Midline(Obstacle):
    def __init__(self, width, height, x, y, color='violet'):
        super().__init__(width, height, x, y, color)
        self.collision_ball = False
        

class DestroyableObstacle(Obstacle):
    def __init__(self, width, height, x, y, color='blue', destroyable=True, max_health = 4):
        super().__init__(width, height, x, y, color, destroyable)
        self.max_health = max_health
        self.current_health = max_health
        self.hp_bar = HpBar(max_health, self.rect)

    def draw(self, screen):
        super().draw(screen)
        self.hp_bar.draw(screen)

    def update_hp(self,ball_velocity, max_ball_velocity):
        self.current_health -= super().get_impact_power(ball_velocity,max_ball_velocity)*self.max_health
        if self.current_health > 0:
            self.hp_bar.hp_bar_update(self.current_health)
        else:
            self.kill()
    
    




