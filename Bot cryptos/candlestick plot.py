import sys
sys.path.append( 'C:/Repositorios/Python' )
sys.path.append( 'H:\Repositorios\Python no github\Bot cryptos' )
import USERBINANCE
import matplotlib.pyplot as plt
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
from binance.client import Client
import numpy as np

client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')

basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin
klines = np.array(client.get_klines(symbol=symbolTicker, interval=Client.KLINE_INTERVAL_4HOUR,limit=100)).astype(np.float64)

def _sopres(df):
    val_high = df['High']
    val_Low = df['Low']
    sop = [df['Low'].loc[0]]
    res = [df['High'].loc[0]]
    n = 0
    for value in val_high:
        if value > res[n]:
            res[n] = value
        else:
            
            if n <= len(res):
                res.append(value)
                n +=1
            else:
                res[n] = value
    return res
            
        




df = pd.DataFrame(klines[:, :5],columns=['Date','Open','High','Low','Close'])
#df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = np.round(df['Date'],5)




y = _sopres(df)
x = [df['Date'].loc[0],df['Date'].iloc[-1]]

fig, ax = plt.subplots()
candlestick_ohlc(ax,df.values , width=10000, colorup='green', colordown='red')

ax.plot(x, y)

ax.set_title('Gráfico de velas japonesas')
ax.set_xlabel('Fecha')
ax.set_ylabel('Precio')

plt.show()
