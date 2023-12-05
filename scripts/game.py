import pygame
from random import randint, seed
from player import Player
from obstacle import Obstacle, Midline
from ball import Ball
from constant_values import (SCREEN_WIDTH, SCREEN_HEIGHT, BORDERS_PARAMETER, LEFT, RIGHT,
                             MAX_HEIGHT_OBSTACLE, MAX_WIDTH_OBSTACLE, BORDER_COLOR)

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dodge-ball')
FPS = 60

MENU = 0
GAME = 1
ENDGAME = 2


def draw(walls, all_objects, players_playing, ball, middle_line):
    # Draw background
    SCREEN.fill('Green')
    for obstacle in all_objects:
        obstacle.draw(SCREEN)
    middle_line.draw_mid(SCREEN)
    for wall in walls:
        wall.draw(SCREEN)
    for player in players_playing:
        player.draw(SCREEN)
    ball.draw(SCREEN)
    players_playing.update()


def generate_undestroyable_obstacles(obstacles, players_playing, undestroyable_obstacles):
    for _ in range(0, 3):
        x = randint(0, SCREEN_WIDTH - MAX_WIDTH_OBSTACLE)
        y = randint(0, SCREEN_HEIGHT - MAX_HEIGHT_OBSTACLE)
        new_obstacle = Obstacle(MAX_WIDTH_OBSTACLE, MAX_HEIGHT_OBSTACLE, x, y)
        collision_detection_group = pygame.sprite.Group()
        collision_detection_group.add(obstacles, players_playing, undestroyable_obstacles)
        while pygame.sprite.spritecollide(new_obstacle, collision_detection_group, False):
            x = randint(0, SCREEN_WIDTH - MAX_WIDTH_OBSTACLE)
            y = randint(0, SCREEN_HEIGHT - MAX_HEIGHT_OBSTACLE)
            new_obstacle = Obstacle(MAX_WIDTH_OBSTACLE, MAX_HEIGHT_OBSTACLE, x, y)
        undestroyable_obstacles.add(new_obstacle)


def check_benched(players_playing, bench, team_left, team_right):
    for player in players_playing:
        if player.bench:
            players_playing.remove(player)
            bench.append(player)
            if player.team == RIGHT:
                team_right.remove(player)
            if player.team == LEFT:
                team_left.remove(player)


def endgame(winner):
    font = pygame.font.Font("freesansbold.ttf", 45)
    over_game = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(SCREEN, (0, 0, 0), over_game)
    over_game_text = font.render("Congratulations!", False,(255, 255, 255))
    over_game_text_rect = over_game_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 45))
    SCREEN.blit(over_game_text, over_game_text_rect)
    if winner:
        won = font.render(" Team Right WON!", False, (255, 255, 255))
    else:
        won = font.render("Team Left WON!", False, (255, 255, 255))
    won_rect = won.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 45))
    SCREEN.blit(won, won_rect)
    pygame.display.flip()


def main():
    running = True
    clock = pygame.time.Clock()

    seed()
    team_with_ball = randint(LEFT, RIGHT)
    team_left = []
    team_right = []
    players_playing = pygame.sprite.Group()
    bench = []

    players_right_offensive_coords = [(3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4),
                                      (7 * SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2),
                                      (3 * SCREEN_WIDTH / 4, 3 * SCREEN_HEIGHT / 4)]
    players_left_defensive_coords = [(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4),
                                     (SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2),
                                     (SCREEN_WIDTH / 4, 3 * SCREEN_HEIGHT / 4)]
    players_right_defensive_coords = [(3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4),
                                      (9 * SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2),
                                      (3 * SCREEN_WIDTH / 4, 3 * SCREEN_HEIGHT / 4)]
    players_left_offensive_coords = [(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4),
                                     (3 * SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2),
                                     (SCREEN_WIDTH / 4, 3 * SCREEN_HEIGHT / 4)]
    if team_with_ball == RIGHT:
        for xy in players_right_offensive_coords:
            team_right.append(Player(RIGHT, xy[0], xy[1]))
        for xy in players_left_defensive_coords:
            team_left.append(Player(LEFT, xy[0], xy[1]))
    else:
        for xy in players_left_offensive_coords:
            team_left.append(Player(LEFT, xy[0], xy[1]))
        for xy in players_right_defensive_coords:
            team_right.append(Player(RIGHT, xy[0], xy[1]))

    print(f"Team with ball: {'RIGHT' if team_with_ball == RIGHT else 'LEFT'}")

    players_playing.add(team_right, team_left)
    ball = Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    walls = pygame.sprite.Group()
    undestroyable_obstacles = pygame.sprite.Group()
    obstacles_player = pygame.sprite.Group()
    all_obstacles = pygame.sprite.Group()

    middle_line = Midline(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH // 2 - BORDERS_PARAMETER // 2, 0, BORDER_COLOR)
    team_right_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH - BORDERS_PARAMETER, 0, BORDER_COLOR)
    team_left_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, 0, 0, BORDER_COLOR)
    up_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, 0, BORDER_COLOR)
    down_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, SCREEN_HEIGHT - BORDERS_PARAMETER, BORDER_COLOR)

    walls.add(team_left_line, team_right_line, up_line, down_line)

    generate_undestroyable_obstacles(all_obstacles, players_playing, undestroyable_obstacles)
    all_obstacles.add(undestroyable_obstacles)

    obstacles_player.add(all_obstacles, middle_line, walls)
    stage = GAME
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        if stage == MENU:
            pass

        elif stage == GAME:
            draw(walls, all_obstacles, players_playing, ball, middle_line)

            if team_left:
                player_in_control = team_left[0]
                player_in_control.move(obstacles_player, players_playing)

            ball.move()
            ball.check_collision_wall()
            ball.check_collision_obstacle(all_obstacles)
            ball.check_collision_player(players_playing)
            check_benched(players_playing, bench, team_left, team_right)

            if not team_left or team_right:
                stage = ENDGAME

        elif stage == ENDGAME:
            if not team_left:
                endgame(team_left)
            if not team_right:
                endgame(team_right)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                for player in bench:
                    if player.team == RIGHT:
                        team_right.append(player)
                    if player.team == LEFT:
                        team_left.append(player)
                ball.rect.move(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                stage = GAME

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
