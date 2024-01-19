import pygame

class Marker(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.color = player.color
        self.rect = self.image.get_rect()
        self.player = player

    def move_marker(self):
        pygame.draw.polygon(self.image, self.color, [(0, 0), (10, 20), (20, 0)])
        player_height = self.player.image.get_height()

        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery - player_height

    def change_player(self, player):
        self.player = player
        self.color = self.player.color
        self.move_marker()
