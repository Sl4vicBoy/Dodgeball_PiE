import pygame
import os
from math import sqrt


class Player(pygame.sprite.Sprite):
    VEL = 4

    player_img_left_direction = None
    player_img_right_direction = None
    player_img_up_direction = None
    player_img_down_direction = None
    player_images = None

    @staticmethod
    def load_player_images():
        player_img = pygame.image.load(os.path.join('Assets', 'players', 'superswinka.png')).convert_alpha()
        player_img_scaled = pygame.transform.scale_by(player_img, 0.4)

        Player.player_img_left_direction = pygame.transform.flip(player_img_scaled, True, False)
        Player.player_img_right_direction = player_img_scaled
        Player.player_img_up_direction = pygame.transform.rotate(player_img_scaled, 90)
        Player.player_img_down_direction = pygame.transform.rotate(player_img_scaled, -90)

        Player.player_images = (Player.player_img_right_direction, Player.player_img_left_direction,
                                Player.player_img_up_direction, Player.player_img_down_direction)

    def __init__(self, team, x, y, bench=False):
        pygame.sprite.Sprite.__init__(self)
        self.team = int(team)
        self.bench = bench

        if team:
            self.color = 'red'
            self.image = Player.player_img_left_direction
        else:
            self.color = 'cyan'
            self.image = Player.player_img_right_direction

        self.rect = self.image.get_rect(center=(x, y))

    def move(self, obstacles, team, marker):
        keys = pygame.key.get_pressed()

        current_x = self.rect.x
        current_y = self.rect.y
        prev_rect = self.rect
        prev_img = self.image

        x_movement = 0
        y_movement = 0

        if self.team:
            if keys[pygame.K_RIGHT]:
                x_movement += self.VEL

            if keys[pygame.K_LEFT]:
                x_movement -= self.VEL

            if keys[pygame.K_UP]:
                y_movement -= self.VEL

            if keys[pygame.K_DOWN]:
                y_movement += self.VEL
        else:
            if keys[pygame.K_d]:
                x_movement += self.VEL

            if keys[pygame.K_a]:
                x_movement -= self.VEL

            if keys[pygame.K_w]:
                y_movement -= self.VEL

            if keys[pygame.K_s]:
                y_movement += self.VEL

        self.rect.x += x_movement
        self.rect.y += y_movement

        obstacle_collision = pygame.sprite.spritecollide(self, obstacles, False, pygame.sprite.collide_mask)
        player_collision = pygame.sprite.spritecollide(self, team, False, pygame.sprite.collide_mask)

        if self in player_collision:
            player_collision.remove(self)

        if obstacle_collision or player_collision:
            self.rect.x, self.rect.y = current_x, current_y
            self.image = prev_img
            self.rect = prev_rect

        marker.move_marker()

    def catch_ball(self, ball, events):
        x = self.rect.centerx
        y = self.rect.centery
        ball_player_distance = sqrt((x - ball.rect.centerx) ** 2 + (y - ball.rect.centery) ** 2)

        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and (ball_player_distance <= 60):
                ball.danger = False
                ball.vel = pygame.math.Vector2(0, 0)
                ball.caught_by_player = self
                return 0
        return 1
