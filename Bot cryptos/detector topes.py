import userbinance
from binance.client import Client
#import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import time
from os import system
import pandas as pd
#from talib import stream as stm
import numpy as np
#import threading
import os.path

def _truncate_(num,n):
    i = int(num * (10**n))/(10**n)
    return float(i)

def _roundplaces_():
    symbolinfo = client.get_symbol_info(symbolTicker)
    
    # Extract tick size and step size
    tick_size = float(symbolinfo['filters'][0]['tickSize'])
    step_size = float(symbolinfo['filters'][1]['stepSize'])

    # Calculate the decimal places for price and quantity
    roundprice = int(-np.log10(tick_size))
    roundqty = int(-np.log10(step_size))

    roundplaceinfo = {'roundprice': roundprice, 'roundqty': roundqty}
    return roundplaceinfo


client = Client(userbinance.API_KEY, userbinance.API_SECRET, tld='com')

basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin

rounds = _roundplaces_()


while 1:
    try:
        system("cls")
        klines = np.array(client.get_klines(symbol=symbolTicker, interval=Client.KLINE_INTERVAL_4HOUR,limit=200)).astype(np.float64)
    except:
        time.sleep(20)
        client = Client(userbinance.API_KEY, userbinance.API_SECRET, tld='com')
        continue

    if len(klines) == 200:
        
        
        Close = klines[-1,4]
        Open = klines[-1,1]
        High = klines[-1,2]
        Low = klines[-1,3]
        print('Close ',Close,' Open ',Open,'High ',High,'Low ',Low)

    time.sleep(1)