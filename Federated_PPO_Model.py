import gym
import numpy as np
from gym import spaces
import random
import torch

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

class GPUSchedulingEnv(gym.Env):
    def __init__(self):
        super(GPUSchedulingEnv).__init__()
        self.observation_space = spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)
        self.action_space = spaces.Box(low=0, high=1, shape=(1,),dtype=np.float32)
        self.state = np.array([0.5, 0.5, 0.5], dtype=np.float32)
        self.step_count = 0
        self.max_steps = 50
    
    def reset(self, *, seed = None, options = None):
        self.state = np.array([random.random(),random.random(),random.random()],dtype=np.float32)
        self.step_count = 0
        return self.state, {}
    
    def step(self, action):
        utilization, energy, speed = self.state
        utilization = np.clip(utilization+(action[0]-0.5)*0.1 + random.uniform(-0.05, 0.05),0 ,1)
        energy = np.clip(energy-action[0]*0.05+ random.uniform(-0.05, 0.05),0 ,1)
        speed = np.clip(speed+(action[0]-0.5)*0.1+random.uniform(-0.05,0.05),0, 1)
        self.state = np.array([utilization, energy, speed],dtype=np.float32)

        reward = 0.7*utilization+0.2*(1-energy)+0.1*speed
        self.step_count +=1
        done = self.step_count >= self.max_steps
        return self.state, reward, done, False, {}
    
def federated_aggregate(models):
    global_state_dict = {}
    num_models = len(models)

    for key, params in models[0].policy.state_dict().items():
        global_state_dict[key] = torch.zeros_like(params)
    
    for model in models:
        local_state = model.policy.state_dict()
        for key in local_state:
            global_state_dict[key] +=local_state[key]
    
    for key in global_state_dict:
        global_state_dict[key] /=num_models
    
    return global_state_dict

def update_local_models(models, global_state_dict):
    for model in models:
        model.policy.load_state_dict(global_state_dict)


def main():
    num_clusters = 50
    local_training_steps = 8000
    aggregation_interval = 1
    num_round =10

    agents = []
    for i in range(num_clusters):
        env = GPUSchedulingEnv()
        model =PPO("MlpPolicy", env, verbose=0)
        agents.append(model)
    
    print("Starting gederated training simulation....")
    for round in range(num_round):
        print(f"\n Federated Round {round+1}/{num_round} -----")
        for idx , agent in enumerate (agents):
            print(f"Training agent {idx+1}/{num_clusters} locally ......")
            agent.learn(total_timesteps=local_training_steps, reset_num_timesteps=False)
        global_state_dict = federated_aggregate(agents)
        update_local_models(agents,global_state_dict)
        print( "Global model aggregated and local models updated.")


    test_env = GPUSchedulingEnv()
    obs, info = test_env.reset()

    total_reward = 0.0
    done = False
    while not done:
        action, _ = agents[0].predict(obs, deterministic=True)
        obs, reward, done, truncated, info = test_env.step(action)
        total_reward += reward
    print(f"\nTest Episode Total Reward (using global model from agent 0): {total_reward:.2f}")

    num_test_episodes = 10
    rewards = []
    for _ in range(num_test_episodes):
        obs, info = test_env.reset()
        obs = np.array(obs)  
        ep_reward = 0
        done = False
        while not done:
            action, _ = agents[0].predict(obs, deterministic=True)
            obs, reward, done, truncated, info = test_env.step(action)
            ep_reward += reward
        rewards.append(ep_reward)
    avg_reward = np.mean(rewards)
    print(f"Average reward over {num_test_episodes} test episodes: {avg_reward:.2f}")

if __name__ == "__main__":
    main()
