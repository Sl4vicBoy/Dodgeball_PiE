import pygame
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, BORDERS_PARAMETER


class Player(pygame.sprite.Sprite):
    RADIUS = 20
    VEL = 4

    def __init__(self, team, x, y):
        pygame.sprite.Sprite.__init__(self)  # konstruktor klasy bazowej jak cos
        self.team = int(team)
        self.radius = Player.RADIUS
        if team:
            self.color = 'Red'
        else:
            self.color = 'Blue'
        self.image = pygame.Surface((Player.RADIUS * 2, Player.RADIUS * 2))
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        keys = pygame.key.get_pressed()
        match self.team:
            case 1:  # RIGHT
                if keys[pygame.K_RIGHT] and self.rect.centerx + Player.VEL < SCREEN_WIDTH - BORDERS_PARAMETER - Player.RADIUS:
                    self.rect.x += self.VEL
                if keys[pygame.K_LEFT] and self.rect.centerx - Player.VEL > (SCREEN_WIDTH + BORDERS_PARAMETER) / 2 + Player.RADIUS:
                    self.rect.x -= self.VEL

            case 0:  # LEFT
                if keys[pygame.K_RIGHT] and self.rect.centerx + Player.VEL < (
                        SCREEN_WIDTH - BORDERS_PARAMETER) / 2 - Player.RADIUS:
                    self.rect.x += self.VEL
                if keys[pygame.K_LEFT] and self.rect.centerx - Player.VEL > BORDERS_PARAMETER + Player.RADIUS:
                    self.rect.x -= self.VEL

        if keys[pygame.K_UP] and self.rect.centery - Player.VEL > Player.RADIUS + BORDERS_PARAMETER:
            self.rect.y -= Player.VEL
        if keys[pygame.K_DOWN] and self.rect.centery + Player.VEL < SCREEN_HEIGHT - Player.RADIUS - BORDERS_PARAMETER:
            self.rect.y += Player.VEL

    def check_collision(self, team):
        collision = False
        for player in team:
            if pygame.sprite.collide_circle(self, player) and player != self:
                collision = True
        if collision:
            self.color = 'Pink'
        else:
            match self.team:
                case 1:
                    self.color = 'Red'
                case 0:
                    self.color = 'Blue'

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
