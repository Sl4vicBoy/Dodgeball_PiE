import gym
import gym_env

environment = gym.make("DodgeballEnv-v0")

episodes = 10

for episodes in range(1, episodes+1):
    state = environment.reset()
    done = False
    score = 0
    while not done:
        action = environment.action_space.sample()
        _, reward, done, __ = environment.step(action)
        score += reward
        environment.render()
