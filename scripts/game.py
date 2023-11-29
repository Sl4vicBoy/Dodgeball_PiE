import pygame
from random import randint, seed
from player import Player
from obstacle import Obstacle
from ball import Ball
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BORDERS_PARAMETER, LEFT, RIGHT

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dodge-ball')

middle_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH // 2 - BORDERS_PARAMETER // 2, 0)
team_right_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH - BORDERS_PARAMETER, 0)
team_left_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, 0, 0)
up_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, 0)
down_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, SCREEN_HEIGHT - BORDERS_PARAMETER)


def draw(screen, players, ball):
    # Draw background
    screen.fill('Green')
    for player in players:
        player.draw(screen)
    ball.draw(screen)    

    pygame.draw.rect(screen, 'fuchsia', middle_line.return_parameters())
    pygame.draw.rect(screen, 'fuchsia', team_right_line.return_parameters())
    pygame.draw.rect(screen, 'fuchsia', team_left_line.return_parameters())
    pygame.draw.rect(screen, 'fuchsia', up_line.return_parameters())
    pygame.draw.rect(screen, 'fuchsia', down_line.return_parameters())
    pygame.display.update()


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

    # docelowo pozniej sie cos z tym madrego zrobi
    all_players = pygame.sprite.Group()
    all_players.add(team_right, team_left)
    ball = Ball(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 6)

    while running:
        clock.tick(FPS)
        draw(SCREEN, all_players, ball)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        player_in_control = team_left[0]
        player_in_control.move()

        if player_in_control.team == RIGHT:
            player_in_control.check_collision(team_right)
        else:
            player_in_control.check_collision(team_left)

        ball.move()
        ball.handle_collision_wall()
        for player in all_players:
            ball.handle_collision_player(player)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
