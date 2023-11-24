import pygame
from random import random, seed
from player import Player
from obstacle import Obstacle
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge-ball")

LEFT = 0
RIGHT = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
BLUE = (29, 226, 217)
RED = (226, 29, 38)
GREEN = (137, 226, 29)
VIOLET = (118, 29, 226)

BORDERS_PARAMETER = 5

FPS = 60

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
    team_with_ball = random()
    team_right = []
    team_left = []

    # koordy z gory ustalone dla poszczegolnych teamow(punkty spawnu)
    # postacie nie beda sie respic randomowo tylko w okreslonych miejscach w zaleznosci od tego ktora druzyna posiada pilke i zaczyna gre
    players_offensive_coords = [(3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4), (7 * SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2),
                                (3 * SCREEN_WIDTH / 4, 3 * SCREEN_HEIGHT / 4)]
    players_defensive_coords = [(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4), (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 2),
                                (SCREEN_WIDTH / 4, 3 * SCREEN_HEIGHT / 4)]

    if team_with_ball == RIGHT:
        for xy in players_offensive_coords:
            team_right.append(Player(team_right, xy[0], xy[1]))
        for xy in players_defensive_coords:
            team_left.append(Player(team_left, xy[0], xy[1]))
    else:
        for xy in players_offensive_coords:
            team_left.append(Player(team_left, xy[0], xy[1]))
        for xy in players_defensive_coords:
            team_right.append(Player(team_right, xy[0], xy[1]))

    while running:
        # Cap the frame rate
        clock.tick(FPS)
        # Draw background
        draw(SCREEN, team_left + team_right)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
    pygame.quit()


if __name__ == '__main__':
    main()