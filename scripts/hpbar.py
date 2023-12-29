import pygame 
import math 
from constant_values import HP_COLORS

class HpBar(pygame.sprite.Sprite):
    def __init__(self, max_health, obstacle_rect, color='blue', height=5):
        super().__init__()
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.color = color
        self.color_num = 3
        self.health_fraction = self.current_health / self.max_health
        self.rect = pygame.Rect(obstacle_rect.x, obstacle_rect.y - self.height - 2, obstacle_rect.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def hp_bar_update(self, new_health):
        self.current_health = new_health
        self.health_fraction = self.current_health / self.max_health
        self.rect.width = self.rect.width * self.health_fraction
        self.color_num = math.ceil(new_health * (3/self.max_health)) 
        self.color = HP_COLORS[self.color_num]