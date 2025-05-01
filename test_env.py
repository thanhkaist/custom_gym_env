from my_mujoco_env import MyMujocoEnv
import time

env = MyMujocoEnv()
obs = env.reset()


for _ in range(100):
    action = env.action_space.sample()
    # action[0] = 0.0 # Uncomment to test with one joint
    # action[1] = 0.0 # Uncomment to test with one joint
    obs, reward, done, info = env.step(action)
    print (f"Obs: {obs}, Action: {action}, Reward: {reward}, Done: {done}")
    env.render()
    time.sleep(env.dt)  # match real-time
env.close()