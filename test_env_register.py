
import register
import gym
import time

env = gym.make("MyMujocoEnv-v0")
obs = env.reset()


for _ in range(100):
    action = env.action_space.sample()
    action[0] = 0.0
    obs, reward, done, info = env.step(action)
    print (f"Obs: {obs}, Action: {action}, Reward: {reward}, Done: {done}")
    env.render()
    time.sleep(env.dt)  # match real-time
env.close()