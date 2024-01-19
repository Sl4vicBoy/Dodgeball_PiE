from gym.envs.registration import register

register(
    id="Dodgeball-v0",
    entry_point="gym.env.dodgeball.py:DodgeballEnv",
)
