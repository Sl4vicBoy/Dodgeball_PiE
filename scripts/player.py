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
    
    def move(self,obstacles):
        keys = pygame.key.get_pressed()
        current_x = self.rect.x
        current_y = self.rect.y
        
        if keys[pygame.K_RIGHT]:
                self.rect.x += self.VEL
        elif keys[pygame.K_LEFT]:
                self.rect.x -= self.VEL
        elif keys[pygame.K_UP]:
                self.rect.y -= self.VEL
        elif keys[pygame.K_DOWN]:
                self.rect.y += self.VEL
        
        if pygame.sprite.spritecollide(self, obstacles, False):
            self.rect.x, self.rect.y = current_x, current_y


    def check_collision_player(self, team):
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
