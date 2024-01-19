from gym.envs.registration import register

register(
    id="Dodgeball-v0",
    entry_point="env.dodgeball:DodgeballEnv"
)
