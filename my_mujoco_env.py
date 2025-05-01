import os 
import numpy as np
import gym
from gym import spaces 
import mujoco_py


class MyMujocoEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self,frame_skip=5):
        model_path = os.path.join(os.path.dirname(__file__), 'assets', 'my_robot.xml')
        self.model = mujoco_py.load_model_from_path(model_path)
        self.sim = mujoco_py.MjSim(self.model)
        self.viewer = None 

        # One joint option
        # self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape = (2,), dtype=np.float32)
        # self.action_space = spaces.Box(low =-1.0, high = 1.0, shape=(1,), dtype =np.float32)

        # Two joints option
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)
        

        # control frequency
        self.frame_skip = frame_skip
        self.dt = self.sim.model.opt.timestep * self.frame_skip

    def step(self, action):
        self.sim.data.ctrl[:] = action # should be [slide_ctrl, hinge_ctrl]
        
        for _ in range(self.frame_skip):
            self.sim.step()
        obs = self._get_obs()
        reward = self._get_reward(obs)
        done = False
        info = {}
        return obs, reward, done, info
    
    def reset(self):
        self.sim.reset()
        self.sim.data.qpos[:] = 0.0
        self.sim.data.qvel[:] = 0.0
        return self._get_obs()
    
    def render(self, mode='human'):
        if self.viewer is None:
            self.viewer = mujoco_py.MjViewer(self.sim)
            self.viewer.vopt.flags[mujoco_py.const.VIS_JOINT] = 1  # show joint axes
            
        self.viewer.render()
        if mode == 'rgb_array':
            return self.sim.render(mode='rgb_array')
        return None 
    
    def close(self):
        if self.viewer is not None:
            del self.viewer
            self.viewer = None 

    def _get_obs(self):
        return np.array([
        self.sim.data.qpos[0],  # slide pos
        self.sim.data.qvel[0],  # slide vel
        self.sim.data.qpos[1],  # hinge pos (angle)
        self.sim.data.qvel[1],  # hinge vel
        ], dtype=np.float32)
    
    def _get_reward(self, obs):
        # Define your reward function here
        # For example, you can return the negative distance to a target position
        target_pos = 0
        target_pos1 = 0
        pos = self.sim.data.qpos[0]
        pos1 = self.sim.data.qpos[1]
        return -np.abs(pos - target_pos) - np.abs(pos1 - target_pos1)
