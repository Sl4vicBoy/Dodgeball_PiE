import pygame
RADIUS = 20

class Player:
    def __init__(self, team, x, y):
        self.team = team
        self.x = y
        self.y = x
        self.radius = RADIUS
        if team:
            self.color = (29, 226, 217)
        else:
            self.color = (226, 29, 38)
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)