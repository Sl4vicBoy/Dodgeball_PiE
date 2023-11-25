import pygame
from random import randint, seed
from player import Player
from obstacle import Obstacle
from ball import Ball, handle_collision_wall,handle_collision_players
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




def draw(screen, players,ball):
    # Draw background
    screen.fill(GREEN)
    for player in players:
        player.draw(screen)
    ball.draw(screen)    
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

    # koordy z gory ustalone dla poszczegolnych teamow(punkty spawnu)
    # postacie nie beda sie respic randomowo tylko w okreslonych miejscach w zaleznosci od tego ktora druzyna posiada pilke i zaczyna gre
    players_offensive_coords = [(3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4), (7 * SCREEN_WIDTH / 10, SCREEN_HEIGHT / 2),
                                (3 * SCREEN_WIDTH / 4, 3 * SCREEN_HEIGHT / 4)]
    players_defensive_coords = [(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4), (SCREEN_WIDTH / 5, SCREEN_HEIGHT / 2),
                                (SCREEN_WIDTH / 4, 3 * SCREEN_HEIGHT / 4)]

    if team_with_ball == RIGHT:
        for xy in players_offensive_coords:
            team_right.append(Player(RIGHT, xy[0], xy[1]))
        for xy in players_defensive_coords:
            team_left.append(Player(LEFT, xy[0], xy[1]))
    else:
        for xy in players_offensive_coords:
            team_left.append(Player(LEFT, xy[0], xy[1]))
        for xy in players_defensive_coords:
            team_right.append(Player(RIGHT, xy[0], xy[1]))
    print(f"Team with ball: {'RIGHT' if team_with_ball == RIGHT else 'LEFT'}")
    
    ball=Ball(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,10)#dodajemy pilke

    while running:
        clock.tick(FPS)
        draw(SCREEN, team_left + team_right,ball)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        player_in_control = team_left[0]
        player_in_control.move()
        ball.move()#pilka sie rusza
        handle_collision_wall(ball)#pilka omija przeszkody
        for player in team_left + team_right:
            handle_collision_players(ball, player)

    pygame.quit()


if __name__ == '__main__':
    main()