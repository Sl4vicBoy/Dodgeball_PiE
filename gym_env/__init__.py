from gym.envs.registration import register

register(
    id="DodgeballEnv-v0",
    entry_point="gym_env.env.dodgeball:DodgeballEnv"
)
