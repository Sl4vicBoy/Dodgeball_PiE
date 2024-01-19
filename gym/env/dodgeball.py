import gym
import numpy as np
import pygame
from random import randint
from player import Player
from obstacle import Obstacle, Midline, HpObstacle
from ball import Ball
from constant_values import (SCREEN_WIDTH, SCREEN_HEIGHT, BORDERS_PARAMETER, LEFT, RIGHT,
                             MAX_HEIGHT_OBSTACLE, MAX_WIDTH_OBSTACLE, BORDER_COLOR, SCOREBOARD)
from marker import Marker
from gym import spaces

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + SCOREBOARD))
pygame.display.set_caption('Dodge-ball')
Player.load_player_images()


def check_benched(players_playing, bench_left, bench_right, team_left, team_right):
    for player in players_playing:
        if player.bench:
            players_playing.remove(player)
            if player.team == RIGHT:
                player.image = Player.player_images[1]
                team_right.remove(player)
                bench_right.append(player)
            if player.team == LEFT:
                player.image = Player.player_images[0]
                team_left.remove(player)
                bench_left.append(player)
            player.rect = player.image.get_rect()

    width = Player.player_img_left_direction.get_width()
    for count, player in enumerate(bench_left):
        player.rect.center = (SCOREBOARD / 2 + width * count, SCREEN_HEIGHT + SCOREBOARD / 2)
    for count, player in enumerate(bench_right):
        player.rect.center = (SCREEN_WIDTH - (SCOREBOARD / 2 + width * count), SCREEN_HEIGHT + SCOREBOARD / 2)


def change_player(team, player_in_control, marker):
    index = team.index(player_in_control)
    if index + 1 >= len(team):
        player_in_control = team[0]
    else:
        player_in_control = team[index + 1]
    marker.change_player(player_in_control)
    return player_in_control


class DodgeballEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10}

    def __init__(self):
        super(DodgeballEnv, self).__init__()

        self.ball = None
        self.all_players = None
        self.bench_left = None
        self.bench_right = None
        self.players_playing = None
        self.marker_left = None
        self.marker_right = None
        self.walls = None
        self.map_obstacles = None
        self.obstacles_player = None
        self.ball_obstacles = None
        self.ball_sprite = None
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
        self.is_caught = 0
        self.num_players = 6

        self.action_space = spaces.Dict({
            "move": Tuple([
                Box(low=-10, high=10, shape=(2,), dtype=np.float32),
                Box(low=-10, high=10, shape=(2,), dtype=np.float32),
                Discrete(2),
                Discrete(2)
            ]),
            "throw": Tuple([
                Box(low=np.radians(-90), high=np.radians(90), shape=(1,), dtype=np.float32),
                Box(low=-10, high=10, shape=(2,), dtype=np.float32),
                Discrete(2)
            ])
        })
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.num_players * 2 + 4,), dtype=np.float32)

        self.window = None
        self.clock = None

    def _get_info(self):
        pass

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_players = pygame.sprite.Group()

        self.team_left = []
        self.team_right = []

        self.bench_left = []
        self.bench_right = []

        self.walls = pygame.sprite.Group()
        self.map_obstacles = pygame.sprite.Group()
        self.obstacles_player = pygame.sprite.Group()
        self.ball_obstacles = pygame.sprite.Group()
        self.ball_sprite = pygame.sprite.GroupSingle()
        self.players_playing = pygame.sprite.Group()

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
        self.ball_sprite.add(self.ball)

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

        self.all_players.add(self.team_right, self.team_left)
        self.players_playing.add(self.all_players)

        self.obstacles_player.add(self.walls, self.middle_line)
        self.generate_obstacles()
        self.obstacles_player.add(self.map_obstacles)

        self.ball_obstacles.add(self.map_obstacles, self.walls)
        self.ball.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        if team_with_ball == LEFT:
            self.ball.def_vel(-4, 0)
            self.ball.danger = RIGHT
        if team_with_ball == RIGHT:
            self.ball.def_vel(4, 0)
            self.ball.danger = LEFT

        self.marker_sprite = pygame.sprite.Group()
        self.marker_left = Marker(self.team_left[0])
        self.marker_right = Marker(self.team_right[0])
        self.marker_sprite.add(self.marker_left, self.marker_right)

        self.player_controlled_left = self.team_left[0]
        self.player_controlled_right = self.team_right[0]

        observation = None
        info = None

        return observation, info

    def step(self, action):
        if self.ball.caught_by_player is None:
            move_vector_right, move_vector_left, switch_right, switch_left = action["move"]
            if switch_right:
                self.player_controlled_right = change_player(self.team_right, self.player_controlled_right,
                                                             self.marker_right)
            if switch_left:
                self.player_controlled_left = change_player(self.team_left, self.player_controlled_left,
                                                            self.marker_left)
            self.player_controlled_right.move(move_vector_right, self.marker_right, self.obstacles_player,
                                              self.team_right)
            self.player_controlled_left.move(move_vector_left, self.marker_left, self.obstacles_player, self.team_left)
            self.player_controlled_left.catch_ball(self.ball)
            self.player_controlled_right.catch_ball(self.ball)
        else:
            throwing_angle, move_vector, switch = action["throw"]
            if self.ball.caught_by_player.team == RIGHT:
                if switch:
                    self.player_controlled_left = change_player(self.team_left,
                                                  self.player_controlled_left, self.marker_left)
                self.player_controlled_left.move(move_vector, self.marker_left, self.obstacles_player, self.team_left)
            else:
                if switch:
                    self.player_controlled_right = change_player(self.team_right,
                                                                self.player_controlled_right, self.marker_right)
                self.player_controlled_right.move(move_vector, self.marker_left, self.obstacles_player, self.team_right)
            self.ball.throw_a_ball(throwing_angle)

        self.ball.move()
        self.ball.maintain_collision_obstacle(self.ball_obstacles, self.players_playing)

        terminated = False

        if self.ball.check_collision_obstacle(self.ball_obstacles, self.players_playing):
            check_benched(self.players_playing, self.bench_left, self.bench_right, self.team_left, self.team_right)

        if not self.team_left or not self.team_right:
            terminated = True

        observation = self._get_observation()
        reward = 0 if self.ball.caught_by_player is None else 1
        info = None  # jakies get info mozemy zaimplementowac
        return observation, reward, terminated, False, info

    def render(self):  # tu jest rysowanie i ustawianie wszystkiego -> pygame
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

        ball_data = [self.ball.rect.x, self.ball.rect.y, self.is_caught]

        observation = np.array(player_data + ball_data, dtype=np.float32)

        return observation
    
    def get_high(self):
        player_xy_high = np.array([600, 800]*self.num_players, dtype=np.float32)
        ball_xy_high = np.array([600, 800], dtype=np.float32)
        is_caught_high = 1

        return np.concatenate([player_xy_high, ball_xy_high, is_caught_high])
    
    def get_low(self):
        player_xy_low = np.array([0, 0]*self.num_players, dtype=np.float32)
        ball_xy_low = np.array([0, 0], dtype=np.float32)
        is_caught_low = 0

        return np.concatenate([player_xy_low, ball_xy_low, is_caught_low])

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    def generate_obstacles(self):
        for coord in [(100, 100), (570, 470), (450, 300)]:
            x, y = coord
            new_obstacle = Obstacle(MAX_WIDTH_OBSTACLE, MAX_HEIGHT_OBSTACLE, x, y)
            self.map_obstacles.add(new_obstacle)

        for coord in [(430, 120), (300, 400), (120, 320)]:
            x, y = coord
            new_obstacle = HpObstacle(MAX_WIDTH_OBSTACLE, MAX_HEIGHT_OBSTACLE, x, y)
            self.map_obstacles.add(new_obstacle)
