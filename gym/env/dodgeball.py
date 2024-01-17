import gym
from gym import spaces
import numpy as np
import pygame
from random import randint, seed
from player import Player
from obstacle import Obstacle, Midline, HpObstacle
from ball import Ball, Cue
from constant_values import (SCREEN_WIDTH, SCREEN_HEIGHT, BORDERS_PARAMETER, LEFT, RIGHT, NONE,
                             MAX_HEIGHT_OBSTACLE, MAX_WIDTH_OBSTACLE, BORDER_COLOR, SCOREBOARD)
from marker import Marker

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + SCOREBOARD))
pygame.display.set_caption('Dodge-ball')
Player.load_player_images()


class DodgeballEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    def __init__(self):
        super(DodgeballEnv, self).__init__()
        self.cue = None
        self.ball = None
        self.all_players = None
        self.marker_left = None
        self.marker_right = None
        self.walls = None
        self.map_obstacles = None
        self.obstacles_player = None
        self.ball_obstacles = None
        self.ball_sprite = None
        self.cue_sprite = None
        self.marker_sprite = None
        self.middle_line = None
        self.team_right_line = None
        self.team_left_line = None
        self.up_line = None
        self.down_line = None

        self.team_right = None
        self.team_left = None
        self.player_controlled_left = None
        self.player_controlled_right = None

        self.num_players = 6
        self.action_space = spaces.Discrete(10)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.num_players * 2 + 4,), dtype=np.float32)

        self.window = None
        self.clock = None

    def _get_info(self):
        pass

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_players = pygame.sprite.Group()

        self.walls = pygame.sprite.Group()
        self.map_obstacles = pygame.sprite.Group()
        self.obstacles_player = pygame.sprite.Group()
        self.ball_obstacles = pygame.sprite.Group()
        self.ball_sprite = pygame.sprite.GroupSingle()
        self.cue_sprite = pygame.sprite.GroupSingle()

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

        self.middle_line = Midline(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH // 2 - BORDERS_PARAMETER // 2, 0,
                                   BORDER_COLOR)
        self.team_right_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, SCREEN_WIDTH - BORDERS_PARAMETER, 0,
                                        BORDER_COLOR)
        self.team_left_line = Obstacle(BORDERS_PARAMETER, SCREEN_HEIGHT, 0, 0, BORDER_COLOR)
        self.up_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, 0, BORDER_COLOR)
        self.down_line = Obstacle(SCREEN_WIDTH, BORDERS_PARAMETER, 0, SCREEN_HEIGHT - BORDERS_PARAMETER, BORDER_COLOR)

        self.walls.add(self.team_left_line, self.team_right_line, self.up_line, self.down_line)

        self.cue = Cue(self.ball.rect.center)
        self.ball_sprite.add(self.ball)
        self.cue_sprite.add(self.cue)

        team_with_ball = randint(LEFT, RIGHT)
        if team_with_ball == RIGHT:
            for xy in players_right_offensive_coords:
                self.team_right.append(Player(RIGHT, xy[0], xy[1]))
            for xy in players_left_defensive_coords:
                self.team_left.append(Player(LEFT, xy[0], xy[1]))
        else:
            for xy in players_left_offensive_coords:
                self.team_left.append(Player(LEFT, xy[0], xy[1]))
            for xy in players_right_defensive_coords:
                self.team_right.append(Player(RIGHT, xy[0], xy[1]))

        self.all_players.add(team_right, team_left)
        self.players_playing.add(self.all_players)

        self.obstacles_player.add(walls, middle_line)
        self.generate_obstacles()
        self.obstacles_player.add(self.map_obstacles)

        self.ball_obstacles.add(map_obstacles, walls)
        self.ball.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        if team_with_ball == LEFT:
            self.ball.def_vel(-4, 0)
            self.ball.danger = RIGHT
        if team_with_ball == RIGHT:
            self.ball.def_vel(4, 0)
            self.ball.danger = LEFT

        self.marker_sprite = pygame.sprite.Group()
        self.marker_left = Marker(team_left[0])
        self.marker_right = Marker(team_right[0])
        self.marker_sprite.add(marker_left, marker_right)

        self.player_controlled_left = self.team_left[0]
        self.player_controlled_right = self.team_right[0]

        observation = None
        info = None

        return observation, info

    def step(self, action):
        self.ball.move(self.cue)

    def render(self, mode="human"):  # tu jest rysowanie i ustawianie wszystkiego -> pygame
        if self.window is None:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + SCOREBOARD))
            pygame.display.set_caption('Dodge-ball')
            Player.load_player_images()
        if self.clock is None:
            self.clock = pygame.time.Clock()

        SCREEN.fill('Green')

        self.obstacles_player.draw()
        self.all_players.draw(SCREEN)
        self.marker_sprite.draw(SCREEN)
        self.ball.draw(SCREEN)
        self.all_players.update()

        pygame.event.pump()
        pygame.display.update()
        self.clock.tick(self.metadata["render_fps"])

    def _get_observation(self):
        player_data = []
        for player in self.all_players:
            player_data.extend([player.rect.x, player.rect.y])

        ball_data = [self.ball.rect.x, self.ball.rect.y]

        obstacle_data = []  # tu petla for na polozenie wszystkich obstacles

        observation = np.array(player_data + ball_data, dtype=np.float32)

        return observation

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    def generate_obstacles(self, map_obstacles):
        for coord in [(100, 100), (570, 470), (450, 300)]:
            x, y = coord
            new_obstacle = Obstacle(MAX_WIDTH_OBSTACLE, MAX_HEIGHT_OBSTACLE, x, y)
            self.map_obstacles.add(new_obstacle)

        for coord in [(430, 120), (300, 400), (120, 320)]:
            x, y = coord
            new_obstacle = HpObstacle(MAX_WIDTH_OBSTACLE, MAX_HEIGHT_OBSTACLE, x, y)
            self.map_obstacles.add(new_obstacle)
