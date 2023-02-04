import multiprocessing
import os
import pickle
import neat
import numpy as np
from gym import spaces
from gym.utils import seeding
import pandas as pd
from gym import Env
import matplotlib.pyplot as plt
from enum import Enum


def tres(z):
    if z > 5000.0:
        return 1
    if z < 5000.0 and z > 0.0:
        return 2
    else:
        return 0



class Actions(Enum):
    Sell = 1
    Wait = 0
    Buy = 2

class Look(Enum):
    Sell = 1
    Buy = 2

    def opposite(self):
        return Look.Sell if self == Look.Buy else Look.Buy

class Testbot(Env):
    def __init__(self,df,frame_bound):
        assert len(frame_bound) == 2
        assert df.ndim == 2
        
        self.frame_bound = frame_bound
        self.seed()
        self.df = df
        self.prices, self.signal_features = self._process_data()
        self.shape = (1,)
        
        # spaces
        self.action_space = spaces.Discrete(len(Actions))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=self.shape, dtype=np.float32)

        # episode
        self._start_tick = 0
        self._end_tick = len(self.prices) - 1
        self._done = None
        self._current_tick = None
        self._last_trade_tick = None
        self._total_reward = None
        self._first_rendering = None
        self.history = None
        
        self.inv = None
        self.qty = None
        self._look = None
        self.prev_inv = None


    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def reset(self):
        self._done = False
        self._current_tick = self._start_tick
        self._last_trade_tick = None
        self._total_reward = 0.
        self._first_rendering = True
        self.history = {}
        self.inv = 500
        self.qty = 0
        self._look = Look.Buy
        self.prev_inv = 0
        return self._get_observation()


    def step(self, action):
        self._done = False
        
        if self._current_tick == self._end_tick:
            self._done = True

        #print(str(self.inv))
        #print(str(self.inv)+' = 10 ')
        #print(str(action)+' = '+str(Actions.Buy.value))
        #print(str(self._look)+' = '+str(Look.Buy.value))
        
        #COMPRA
        #print(action[0],' === ',self._look.value)
        if action[0] == self._look.value:
            self.prev_inv = self.inv
            self.qty = np.round(((self.inv / self.prices[self._current_tick]) * 0.999),4)
            self.inv = self.inv - (self.qty * self.prices[self._current_tick])
            self._look = self._look.opposite()
        
        #VENTA
        
        step_reward = self._calculate_reward(action)
        #self._total_reward += step_reward
            
        observation = self._get_observation()
        
        self._current_tick += 1
        return observation, step_reward, self._done


    def _get_observation(self):
        return self.signal_features[self._current_tick]


    #def _update_history(self, info):
    #    if not self.history:
    #        self.history = {key: [] for key in info.keys()}
    #
    #    for key, value in info.items():
    #        self.history[key].append(value)
        

    def _process_data(self):
        prices = self.df.loc[:,'Close'].to_numpy()[self.frame_bound[0]:self.frame_bound[1]]
        
        signal_features = self.df.loc[:, ['RSI','STOCHRSIK','STOCHRSID','BBUPPER','BBMIDDLE','BBLOWER']].to_numpy()[self.frame_bound[0]:self.frame_bound[1]]
        return prices,signal_features


    def _calculate_reward(self, action):
        step_reward = 0  # pip

        #print(str(self.qty))
        #print(str(action))
        #print(str(self._look))
        #print(action,'  ==  ',Actions.Sell.value)
        #print('PASS')
        
        if action[0] == self._look.value:
            #print('*****************venta************************')
            self.inv = np.round(((self.qty * self.prices[self._current_tick]) * 0.999),2)
            step_reward = np.round(self.inv-self.prev_inv,2)
            self.qty = 0
            self.prev_inv = 0
            self._look = self._look.opposite()
        return step_reward
    


df = pd.read_csv('ETHUSDT15min6monthn.csv')
df.fillna(0, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df["RSI"] = pd.to_numeric(df["RSI"])
df["STOCHRSIK"] = pd.to_numeric(df["STOCHRSIK"])
df["STOCHRSID"] = pd.to_numeric(df["STOCHRSID"])
df["BBUPPER"] = pd.to_numeric(df["BBUPPER"])
df["BBMIDDLE"] = pd.to_numeric(df["BBMIDDLE"])
df["BBLOWER"] = pd.to_numeric(df["BBLOWER"])
df.set_index('Date', inplace=True)