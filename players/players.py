import pygame
import os
import random


pygame.init()

#jak zmienisz to mapa sie sama dostosuje elo
#consty (kwasny nie lubi krotek)
left=(0)
right=(1)
screen_width, screen_height = (800),(600)
middle_line_width = (10)
border_parameters = (5)

class Player(pygame.sprite.Sprite):
    def __init__(self,team,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'superswinka.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.team = team

    
class Obstacle:
    def __init__(self, width, height, x, y):
        self.obstacle_width = width
        self.obstacle_height = height
        self.obstacle_x = x
        self.obstacle_y = y
    def return_parameters(self):
        return self.obstacle_x, self.obstacle_y, self.obstacle_width, self.obstacle_height
    

middle_line = Obstacle(middle_line_width,screen_height,screen_width//2 - middle_line_width//2,0)
right_line =  Obstacle(border_parameters,screen_height,screen_width-border_parameters,0)
left_line = Obstacle(border_parameters,screen_height,0,0)
up_line = Obstacle(screen_width,border_parameters,0,0)
down_line = Obstacle(screen_width,border_parameters,0,screen_height-border_parameters)


        

# Set up display

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Display Image")

black = (0, 0, 0)
white = (255, 255, 255)
pink = (255, 192, 203)


player_width, player_height = 305, 209

#maksymalne range na potem(poza te koordy postacie nie moga wychodzic; kolizja z dotykaniem sie bedzie tez pozniej xD)
range_x_right = (player_width // 2, screen_width - player_width // 2)
range_x_left = ()
range_y = (player_height // 2, screen_height - player_height // 2)

#zmienna ball ktora mowi po czyjej stronie jest pilka
ball=right

#listy na playerow dla druzyn prawej i lewej
#ogolnie z gory ustalilismy na razie ze sa po 3 osoby w kazdym teamie - do ewentualnej zmiany to jest
team_right = []
team_left = []

#koordy z gory ustalone dla poszczegolnych teamow(punkty spawnu)
#postacie nie beda sie respic randomowo tylko w okreslonych miejscach w zaleznosci od tego ktora druzyna posiada pilke i zaczyna gre
players_offensive_coords = [(3*screen_width/4, screen_height/4),(7*screen_width/10,  screen_height/2),(3*screen_width/4, 3*screen_height/4)]
players_defensive_coords = [(screen_width/4, screen_height/4),(screen_width/5, screen_height/2),(screen_width/4, 3*screen_height/4)]

if (ball==right):
    for xy in players_offensive_coords:
        team_right.append(Player(right, xy[0],xy[1]))
    for xy in players_defensive_coords:
        team_left.append(Player(left, xy[0],xy[1]))
else:
    for xy in players_offensive_coords:
        team_left.append(Player(left, xy[0],xy[1]))
    for xy in players_defensive_coords:
        team_right.append(Player(right, xy[0],xy[1]))


all_players = pygame.sprite.Group()
all_players.add(team_right, team_left)


# Game loop
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       

    # Draw background
    screen.fill(black)
    midline_params=middle_line.return_parameters()
    right_line_params = right_line.return_parameters()
    left_line_params = left_line.return_parameters()
    up_line_params = up_line.return_parameters()
    down_line_params = down_line.return_parameters()
    pygame.draw.rect(screen, white,midline_params)
    pygame.draw.rect(screen, pink,right_line_params)
    pygame.draw.rect(screen, pink,left_line_params)
    pygame.draw.rect(screen, pink,up_line_params)
    pygame.draw.rect(screen, pink,down_line_params)
    # Draw player
    all_players.draw(screen)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()

