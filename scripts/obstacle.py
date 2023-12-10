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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Midline(Obstacle):  # linia po srodku
    def __init__(self, width, height, x, y, color='violet'):
        super().__init__(width, height, x, y, color)
        self.collision_ball = False

    def draw_mid(self, screen):
        self.draw(screen)
        

class DestroyableObstacle(Obstacle):
    def __init__(self, width, height, x, y, color, time_to_live):
        super().__init__(width, height, x, y, color)
        self.time_to_live = time_to_live
    
    def destroy(self):
        pass
