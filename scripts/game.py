import pygame
from random import randint, seed
from player import Player
from obstacle import Obstacle, Midline
from ball import Ball
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BORDERS_PARAMETER, LEFT, RIGHT, BORDER_COLOR, MAX_HEIGHT_OBSTACLE, MAX_WIDTH_OBSTACLE

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dodge-ball')


def draw(screen, all_objects, all_players, ball, middle_line):
    # Draw background
    screen.fill('Green')
    for obstacle in all_objects:
        obstacle.draw(screen)
    middle_line.draw_mid(screen)
    for player in all_players:
        player.draw(screen)
    ball.draw(screen)
    all_players.update()


def generate_undestroyable_obstacles(obstacles, all_players, undestroyable_obstacles):
    for _ in range(0, 3):
        x = randint(0, SCREEN_WIDTH - MAX_WIDTH_OBSTACLE)
        y = randint(0, SCREEN_HEIGHT - MAX_HEIGHT_OBSTACLE)
        new_obstacle = Obstacle(MAX_WIDTH_OBSTACLE, MAX_HEIGHT_OBSTACLE, x, y)
        collision_detection_group = pygame.sprite.Group()
        collision_detection_group.add(obstacles, all_players, undestroyable_obstacles)
        while pygame.sprite.spritecollide(new_obstacle, collision_detection_group, False):
            x = randint(0, SCREEN_WIDTH - MAX_WIDTH_OBSTACLE)
            y = randint(0, SCREEN_HEIGHT - MAX_HEIGHT_OBSTACLE)
            new_obstacle = Obstacle(MAX_WIDTH_OBSTACLE, MAX_HEIGHT_OBSTACLE, x, y)
        undestroyable_obstacles.add(new_obstacle)


def main():
    running = True
    clock = pygame.time.Clock()

    seed()
    team_with_ball = randint(LEFT, RIGHT)
    team_left = []
    team_right = []

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

    all_players = pygame.sprite.Group()
    all_players.add(team_right, team_left)
    ball = Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

    middle_line = Midline(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH // 2 - BORDERS_PARAMETER // 2, 0, BORDER_COLOR)
    team_right_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH - BORDERS_PARAMETER, 0, BORDER_COLOR)
    team_left_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, 0, 0, BORDER_COLOR)
    up_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, 0, BORDER_COLOR)
    down_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, SCREEN_HEIGHT - BORDERS_PARAMETER, BORDER_COLOR)
    
    walls = pygame.sprite.Group()
    walls.add(team_left_line, team_right_line, up_line, down_line)

    undestroyable_obstacles = pygame.sprite.Group()

    obstacles_ball = pygame.sprite.Group(walls, undestroyable_obstacles)
    obstacles_player = pygame.sprite.Group(obstacles_ball, middle_line)

    while running:
        clock.tick(FPS)
        draw(SCREEN, obstacles_player, all_players, ball, middle_line)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        player_in_control = team_left[0]
        
        if player_in_control.team == RIGHT:
            player_in_control.move(obstacles_player, team_right)
        else:
            player_in_control.move(obstacles_player, team_left)

        ball.move()
        ball.check_collision_wall()
        ball.check_collision_obstacle(undestroyable_obstacles)
        ball.check_collision_player(all_players)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
