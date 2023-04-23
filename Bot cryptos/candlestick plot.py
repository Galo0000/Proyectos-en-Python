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
nl = 200
basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin
klines = np.array(client.get_klines(symbol=symbolTicker, interval=Client.KLINE_INTERVAL_4HOUR,limit=nl)).astype(np.float64)

def _sopres(df):
    global nl
    val_high = df['High'].astype(int)
    #val_Low = df['Low']
    #sop = [df['Low'].loc[0]]
    res = [0]*nl
    n = 0
    isup = False
    temp = 0
    result = []
    for value in val_high:
        if value > temp:
            res[n] = value
            isup = True
        elif isup:
            isup = False
            n +=1
        temp = value
            
    for a in res:
        if a != 0:
            result.append(a)
            
    for i in range(len(result)):
        result[i] = int(result[i] / 10) * 10
    
    resultfinal = []
    for n in result:
        if result.count(n) >= 3 and n not in resultfinal:
            resultfinal.append(n)
    
    
    return resultfinal
            
        




df = pd.DataFrame(klines[:, :5],columns=['Date','Open','High','Low','Close'])
#df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = np.round(df['Date'],5)



coord = _sopres(df)
x = [df['Date'].iloc[0],df['Date'].iloc[-1]]

fig, ax = plt.subplots()
candlestick_ohlc(ax,df.values , width=10000, colorup='green', colordown='red')

for a in coord:
    ax.plot(x,[a,a])

ax.set_title('Gráfico de velas japonesas')
ax.set_xlabel('Fecha')
ax.set_ylabel('Precio')

plt.show()
