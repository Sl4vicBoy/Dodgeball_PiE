import pygame
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, BORDERS_PARAMETER, RED, BLUE, PINK


class Player(pygame.sprite.Sprite):
    RADIUS = 20
    VEL = 4

    def __init__(self, team, x, y):
        pygame.sprite.Sprite.__init__(self)  # konstruktor klasy bazowej jak cos
        self.team = int(team)
        self.x = x
        self.y = y
        self.center = (x, y)
        self.radius = Player.RADIUS
        if team:
            self.color = RED
        else:
            self.color = BLUE
        self.image = pygame.Surface((Player.RADIUS * 2, Player.RADIUS * 2))
        self.rect = self.image.get_rect(center=self.center)

    def move(self):
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
        self.center = (self.x, self.y)
        self.rect = self.image.get_rect(center=self.center)

    def check_collision(self, team):
        collision = False
        for player in team:
            if pygame.sprite.collide_circle(self, player) and player != self:
                collision = True
        if collision:
            self.color = PINK
        else:
            match self.team:
                case 1:
                    self.color = RED
                case 0:
                    self.color = BLUE

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)
