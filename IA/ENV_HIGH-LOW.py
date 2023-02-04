import numpy as np
from gym import spaces
from gym.utils import seeding
import pandas as pd
from gym import Env
import matplotlib.pyplot as plt


class Testbot(Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, df,frame_bound):
        assert len(frame_bound) == 2
        assert df.ndim == 2
        
        self.frame_bound = frame_bound
        self.seed()
        self.df = df
        self.highprices,self.lowprices, self.signal_features = self._process_data()
        self.shape = (1,self.signal_features.shape[1])

        # spaces
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=self.shape, dtype=np.float32)

        # episode
        self._highlowprice_history = None
        self._start_tick = 0
        self._end_tick = len(self.highprices) -1
        self._done = None
        self._current_tick = None
        self._total_reward = None
        self.history = None
    ########### DEFS DEL BOT ################
    
    ################################################
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def reset(self):
        self._done = False
        self._current_tick = self._start_tick
        self._highlowprice_history = []
        self._total_reward = 0
        self.history = {}
        return self._get_observation()


    def step(self, action):
        self._done = False
        observation = self._get_observation()
        self._current_tick += 1

        if self._current_tick == self._end_tick:
            self._done = True

        
        step_reward = self._calculate_reward(action)
        self._total_reward += step_reward
            
        self._highlowprice_history.append([action[0],action[1],self._current_tick])
        
        info = dict(
            total_reward = self._total_reward,
        )
        self._update_history(info)

        return observation, step_reward, self._done, info


    def _get_observation(self):
        return self.signal_features[self._current_tick]


    def _update_history(self, info):
        if not self.history:
            self.history = {key: [] for key in info.keys()}

        for key, value in info.items():
            self.history[key].append(value)


    def render(self, mode='human'):
        plt.plot(self.highprices)
        plt.plot(self.lowprices)
        
        h = []
        l = []
        ticks = []
        
        for i in range(0,self._end_tick):
            h.append(self._highlowprice_history[i][1])
            l.append(self._highlowprice_history[i][0])
            ticks.append(self._highlowprice_history[i][3])
   
        
        
        plt.plot(ticks, self.highprices[ticks], 'ro')
        plt.plot(ticks, self.lowprices[ticks], 'go')
        
        plt.suptitle(
            "Total Reward: %.6f" % self._total_reward
        )

        
    def close(self):
        plt.close()


    def save_rendering(self, filepath):
        plt.savefig(filepath)
        
    
    def pause_rendering(self):
        plt.show()


    def _process_data(self):
        highprices = self.df.loc[:,'High'].to_numpy()[self.frame_bound[0]:self.frame_bound[1]]
        lowprices = self.df.loc[:,'Low'].to_numpy()[self.frame_bound[0]:self.frame_bound[1]]
        
        signal_features = self.df.loc[:, ['Volume','STOCHRSIK','STOCHRSID','BBUPPER','BBMIDDLE','BBLOWER','ADX']].to_numpy()[self.frame_bound[0]:self.frame_bound[1]]
        return highprices,lowprices,signal_features


    def _calculate_reward(self, action):
        step_reward = 0
        n = 40
        #if action[0] < (self.lowprices[self._current_tick] - n) and action[0] > (self.lowprices[self._current_tick] + n):
        #    step_reward -= 0.5
        #if action[1] < (self.highprices[self._current_tick] - n) and action[1] > (self.highprices[self._current_tick] + n):
        #    step_reward -= 0.5
        if action[0] > (self.lowprices[self._current_tick] - n) and action[0] < (self.lowprices[self._current_tick] + n):
            step_reward += 1
        if action[1] > (self.highprices[self._current_tick] - n) and action[1] < (self.highprices[self._current_tick] + n):
            step_reward += 1
        return step_reward
                


df = pd.read_csv('H:\Guille\Escritorio\Programas Python\BotGuille\ETHUSDTdataklines2h1mtest.csv')
df.fillna(0, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
