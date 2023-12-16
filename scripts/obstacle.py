import pygame.draw
from constant_values import BORDER_COLOR, HP_COLORS

class Obstacle(pygame.sprite.Sprite):  
    def __init__(self, width, height, x, y,  color=BORDER_COLOR, destroyable = 0):
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
        

class Midline(Obstacle):  
    def __init__(self, width, height, x, y, color='violet'):
        super().__init__(width, height, x, y, color)
        self.collision_ball = False


class DestroyableObstacle(Obstacle):
    def __init__(self, width, height, x, y, color='blue', destroyable  = 1):
        super().__init__(width, height, x, y, color, destroyable) 
        self.max_health = 4
        self.current_health = 4
        self.hp_bar = HPBAR(4, self.rect)

    def draw(self, screen):

        super().draw(screen)
        self.hp_bar.draw(screen)

    def update_hp(self,new_health):
        self.current_health = new_health
        if(self.current_health > 0):
            self.hp_bar.update(self.current_health)
        else:
            self.rect.x = -1000
            self.rect.y = -1000
            self.hp_bar.rect.x = -1000
            self.hp_bar.rect.y = -1000

class HPBAR(pygame.sprite.Sprite):
    def __init__(self, max_health, obstacle_rect, color='blue', height=5):
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.obstacle_rect = obstacle_rect
        self.color = color
        self.health_fraction = self.current_health / self.max_health
        self.width = obstacle_rect.width
        self.bar_x = self.obstacle_rect.x
        self.bar_y = self.obstacle_rect.y - self.height - 2
        self.rect = pygame.Rect(self.bar_x, self.bar_y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


    def update(self,new_health):
        self.current_health = new_health
        self.health_fraction = self.current_health / self.max_health
        self.width = self.rect.width * self.health_fraction
        self.rect.width = self.width
        self.color = HP_COLORS[new_health]
        
