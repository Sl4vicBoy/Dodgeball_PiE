import pygame.draw
from random import randint
from constant_values import BORDER_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH


class Obstacle(pygame.sprite.Sprite): #niezniszczalna przeszkoda 
    def __init__(self, width = 10, height = 10, x = 10, y = 10, color = BORDER_COLOR):
        super().__init__() 
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color
        self.collision_ball = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Midline(Obstacle): # linia po srodku 
    def __init__(self, width, height, x, y, color):
        super().__init__(width, height, x, y, color)
        self.collision_ball = False

    def draw_mid(self, screen):
        self.draw(screen)
        

class DestroyableObstacle(Obstacle):
    def __init__(self, width, height, x, y, color, time_to_live):
        super().__init__()
        self.time_to_live = time_to_live
    
    def destroy(self):
        pass


