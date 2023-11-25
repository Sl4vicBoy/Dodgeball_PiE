import pygame
from random import randint, seed
from player import Player
from obstacle import Obstacle
from constant_values import SCREEN_WIDTH, SCREEN_HEIGHT, BORDERS_PARAMETER, LEFT, RIGHT, GREEN, VIOLET

pygame.init()

FPS = 60

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge-ball")

middle_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH // 2 - BORDERS_PARAMETER // 2, 0)
team_right_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH - BORDERS_PARAMETER, 0)
team_left_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, 0, 0)
up_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, 0)
down_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, SCREEN_HEIGHT - BORDERS_PARAMETER)


def draw(screen, players):
    # Draw background
    screen.fill(GREEN)
    for player in players:
        player.draw(screen)
    pygame.draw.rect(screen, VIOLET, middle_line.return_parameters())
    pygame.draw.rect(screen, VIOLET, team_right_line.return_parameters())
    pygame.draw.rect(screen, VIOLET, team_left_line.return_parameters())
    pygame.draw.rect(screen, VIOLET, up_line.return_parameters())
    pygame.draw.rect(screen, VIOLET, down_line.return_parameters())
    pygame.display.update()


# Game loop
def main():
    running = True
    clock = pygame.time.Clock()

    seed()
    team_with_ball = randint(LEFT, RIGHT)
    team_left = []
    team_right = []

    # koordy z gory ustalone dla poszczegolnych teamow(punkty spawnu) postacie nie beda sie respic randomowo tylko w
    # okreslonych miejscach w zaleznosci od tego ktora druzyna posiada pilke i zaczyna gre
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

    while running:
        clock.tick(FPS)
        draw(SCREEN, team_left + team_right)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        player_in_control = team_right[0]

        match player_in_control.team:
            case 1:
                player_in_control.move(team_right)
            case 0:
                player_in_control.move(team_left)

    pygame.quit()


if __name__ == '__main__':
    main()
