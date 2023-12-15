import pygame.draw
from constant_values import BORDER_COLOR


class Obstacle(pygame.sprite.Sprite):  # niezniszczalna przeszkoda
    def __init__(self, width, height, x, y, color=BORDER_COLOR):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.collision_ball = True
        self.destroyable = 0
    def draw(self, screen):
        if(self.destroyable):
            self.draw_hp(screen) 
    


class Midline(Obstacle):  # linia po srodku
    def __init__(self, width, height, x, y, color='violet'):
        super().__init__(width, height, x, y, color)
        self.collision_ball = False
        

class DestroyableObstacle(Obstacle):
    def __init__(self, width, height, x, y, color=BORDER_COLOR):
        super().__init__(width, height, x, y, color)
        self.max_health = 2
        self.current_health = 2
        self.destroyable = 1
        self.hp_bar = HPBAR(2,self.rect)
    def draw(self,screen):
        super().draw(screen)
        self.hp_bar.draw(screen)


class HPBAR:
    def __init__(self, max_health, obstacle_rect, color = 'Black',height = 5):
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.obstacle_rect = obstacle_rect
        self.color = color
        self.health_percentage = self.current_health / self.max_health
        self.width = obstacle_rect.width
        bar_x = self.obstacle_rect.x
        bar_y = self.obstacle_rect.y - self.height - 2
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = bar_x
        self.rect.y = bar_y
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)
    



