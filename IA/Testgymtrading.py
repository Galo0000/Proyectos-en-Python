import gym
import gym_anytrading

# Stable baselines - rl stuff
from stable_baselines.common.vec_env import DummyVecEnv
#from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines import A2C
from gym_anytrading.envs import ForexEnv,StocksEnv

# Processing libraries
import numpy as np
from matplotlib import pyplot as plt
#from finta import TA
import pandas as pd



basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin
startx = 210
dklines = False
maxprofit = 0.0
tempprofit = 0.0
modelexist = False


df = pd.read_csv('H:\Guille\Escritorio\Programas Python\ETHUSDTdataklines4h6mtest.csv')
df.fillna(0, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

df.fillna(0, inplace=True)


# ENTRENAMIENTO
timesteps = 100
reg = pd.DataFrame(columns=['timesteps','profits'])

env_maker = lambda: gym.make('forex-v0', df=df, frame_bound=(startx,len(df)-200), window_size=20)
env = DummyVecEnv([env_maker])
model = A2C('MlpLstmPolicy', env, verbose=1)

for i in range(1,10):
  model.learn(total_timesteps=100)
  # EVALUACION
  env = gym.make('forex-v0',df=df, window_size=20, frame_bound=(len(df)-200,len(df)))
  for a in range(1,100):
      obs = env.reset()
      while True:
          obs = obs[np.newaxis, ...]
          action, _states = model.predict(obs)
          obs, rewards, done, info = env.step(action)
          if done:
              reg = reg.append({'timesteps':timesteps,'profits':info['total_profit'],'rewards':info['total_reward']},ignore_index=True)
              break
  timesteps += 100
  obs = env.reset()
plt.figure(figsize=(50,20))
plt.scatter(reg['timesteps'],reg['profits'],marker = 'o',label = 'profits',color='blue')
plt.xlabel('timesteps')
plt.ylabel('profits')
plt.legend()
plt.grid()
plt.show()
