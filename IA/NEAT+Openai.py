import multiprocessing
import os
import pickle
import neat
import numpy as np
from gym import spaces
import pandas as pd
from gym import Env
from enum import Enum

    
def funcionact(z):
    if z > 0:
        return 1
    else:
        return 0

class Actions(Enum):
    Green = 1
    Red = 0

class Testbot(Env):
    def __init__(self,df,frame_bound,window_size):
        assert len(frame_bound) == 2
        assert df.ndim == 2
        
        self.frame_bound = frame_bound
        self.seed()
        self.df = df
        self.window_size = window_size
        self.prices, self.signal_features = self._process_data()
        self.shape = (window_size, self.signal_features.shape[1])
        
        # spaces
        self.action_space = spaces.Discrete(len(Actions))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=self.shape, dtype=np.float32)

        # episode
        self._start_tick = self.window_size
        self._end_tick = len(self.prices) - 1
        self._done = None
        self._current_tick = None
        self._total_reward = None
        


    def reset(self):
        self._done = False
        self._current_tick = self._start_tick
        self._total_reward = 0.
        return self._get_observation()


    def step(self, action):
        self._done = False
        
        self._current_tick += 1
        
        if self._current_tick == self._end_tick:
            self._done = True

        if ((action == Actions.Green.value and self.prices[self._current_tick] > self.prices[self._current_tick-1]) or (action == Actions.Red.value and self.prices[self._current_tick] < self.prices[self._current_tick-1])):
            reward = 1
        else:
            reward = -1
            
        observation = self._get_observation()
        
        return observation, reward, self._done


    def _get_observation(self):
        return np.reshape(self.signal_features[(self._current_tick-self.window_size+1):self._current_tick+1],30)

    def _process_data(self):
        prices = self.df.loc[:,'Close'].to_numpy()[self.frame_bound[0]:self.frame_bound[1]]
        
        signal_features = self.df.loc[:, ['Close','Open','High','Low','Volume']].to_numpy()[self.frame_bound[0]:self.frame_bound[1]]
        return prices,signal_features


df = pd.read_csv('ETHUSDT15min6monthn.csv')
df.fillna(0, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df["RSI"] = pd.to_numeric(df["RSI"])
df["STOCHRSIK"] = pd.to_numeric(df["STOCHRSIK"])
df["STOCHRSID"] = pd.to_numeric(df["STOCHRSID"])
df["MACDh"] = pd.to_numeric(df["MACDh"])
df["Close"] = pd.to_numeric(df["Close"])
df.set_index('Date', inplace=True)



# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    env = Testbot(df,(40,500),6)

    observation = env.reset()
    fitness = 0
    done = False
    while not done:

        action = np.argmax(np.array(net.activate(observation)))
        #print(action)
        observation, reward, done = env.step(action)
        #print(obs)
        
        fitness += reward

    return fitness



def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    
    ### agrega la nueva funcion de activacion?
    #config.genome_config.add_activation('myf', funcionact)
    
    
    
    
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10000))
    
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = p.run(pe.evaluate)
    
    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

    #visualize.plot_stats(stats, ylog=False, view=True)
    #visualize.plot_species(stats, view=True)



if __name__ == '__main__':
    run()