import gym
import gym_env

environment = gym.make("DodgeballEnv-v0")

episodes = 10

for episodes in range(1, episodes+1):
    state, information = environment.reset()
    done = False
    score = 0
    while not done:
        action = environment.action_space.sample()
        obs, reward, done, info = environment.step(action)
        score += reward
        environment.render()
