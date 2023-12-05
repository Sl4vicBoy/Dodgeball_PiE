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
    
    def check_collision_player(self, team):
        collision = False
        for player in team:
            if pygame.sprite.collide_circle(self, player) and player != self:
                collision = True
        return collision

    def move(self, obstacles, team):
        keys = pygame.key.get_pressed()
        current_x = self.rect.x
        current_y = self.rect.y

        x_movement = 0
        y_movement = 0

        if keys[pygame.K_RIGHT]:
            x_movement += self.VEL
        if keys[pygame.K_LEFT]:
            x_movement -= self.VEL
        if keys[pygame.K_UP]:
            y_movement -= self.VEL
        if keys[pygame.K_DOWN]:
            y_movement += self.VEL

        self.rect.x += x_movement
        self.rect.y += y_movement

        if pygame.sprite.spritecollide(self, obstacles, False) or self.check_collision_player(team):
            self.rect.x, self.rect.y = current_x, current_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
