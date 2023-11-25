import pygame
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, BORDERS_PARAMETER, RED, BLUE


class Player:
    RADIUS = 20
    VEL = 4

    def __init__(self, team, x, y):
        self.team = int(team)
        self.x = x
        self.y = y
        self.radius = Player.RADIUS
        if team:
            self.color = RED
        else:
            self.color = BLUE

    def move(self, team):
        keys = pygame.key.get_pressed()

        match self.team:
            case 1:  # RIGHT
                if keys[pygame.K_LEFT] and self.x - Player.VEL > (
                        SCREEN_WIDTH + BORDERS_PARAMETER) / 2 + Player.RADIUS:
                    self.x -= Player.VEL
                if keys[pygame.K_RIGHT] and self.x + Player.VEL < SCREEN_WIDTH - BORDERS_PARAMETER - Player.RADIUS:
                    self.x += Player.VEL

            case 0:  # LEFT
                if keys[pygame.K_LEFT] and self.x - Player.VEL > BORDERS_PARAMETER + Player.RADIUS:
                    self.x -= Player.VEL
                if keys[pygame.K_RIGHT] and self.x + Player.VEL < (
                        SCREEN_WIDTH - BORDERS_PARAMETER) / 2 - Player.RADIUS:
                    self.x += Player.VEL

        if keys[pygame.K_UP] and self.y - Player.VEL > Player.RADIUS + BORDERS_PARAMETER:
            self.y -= Player.VEL
        if keys[pygame.K_DOWN] and self.y + Player.VEL < SCREEN_HEIGHT - Player.RADIUS - BORDERS_PARAMETER:
            self.y += Player.VEL

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
