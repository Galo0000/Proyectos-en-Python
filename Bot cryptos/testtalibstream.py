import USERBINANCE
from binance.client import Client
import talib
from talib import stream as stm
import numpy as np


client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')

basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin
while True:
    klines = np.array(client.get_klines(symbol=symbolTicker, interval=Client.KLINE_INTERVAL_4HOUR,limit=200)).astype(np.float64)
    if len(klines) == 200:
        rsi_stream = stm.RSI(klines[:,4],14)
        rsi_local = talib.RSI(klines[:,4],14)[-1]
        macd_local = talib.MACD((klines[:,4]),fastperiod=12, slowperiod=26, signalperiod=9)
        #print('Normal : ',rsi_local)
        #print('Stream : ',rsi_local)
        print(macd_local[-1][-1])