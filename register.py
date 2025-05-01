from gym.envs.registration import register

# register(
#     id='MyMujocoEnv-v0',
#     entry_point='CustomMujocoEnv.my_mujoco_env:MyMujocoEnv',
# )


register(
    id='MyMujocoEnv-v0',
    entry_point='my_mujoco_env:MyMujocoEnv',
)