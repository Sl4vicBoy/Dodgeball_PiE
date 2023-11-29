import pygame.draw


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
