import gym
from env.dodgeball import DodgeballEnv

environment = gym.make("Dodgeball-v0", render_mode="human")

episodes = 10

for episodes in range(1, episodes +1):
    state = env.reset()
    done = False
    score = 0
    while not done:
        action = env.action_space.sample()
        _, reward, done, __ = environment.step(action)
        score += reward
        environment.render()
