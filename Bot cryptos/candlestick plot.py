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
nl = 100
rep = 1
cercania = 3
basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin
klines = np.array(client.get_klines(symbol=symbolTicker, interval=Client.KLINE_INTERVAL_4HOUR ,limit=nl)).astype(np.float64)

def _redo(l):
    prom = []
    complete = []
    for a in l:
        temp = []
        for b in l:
            if b not in complete:
                if (int(a/10)*10) == (int(b/10)*10):
                    temp.append(b)
                    complete.append(b)
        if len(temp) > 2:
            print(temp)
            prom.append(int(sum(temp)/len(temp)))
            
    #prom = []
    #complete = []
    #for a in l:
    #    temp = []
    #    for b in l:
    #        if b not in temp:
    #            inter = np.intersect1d(b, a)
    #            if inter.size > 2:
    #                temp.append(b)
    #            else:
    #                break
    #    for r in temp:
    #        arreglo_rango = np.array(r)
    #        promedio_rango = np.mean(arreglo_rango)
    #        complete.append(promedio_rango)
    return prom

def _res(df):
    val_high = df['High']
    val_o1 = df['Open'].astype(int)
    val_o2 = df['Close'].astype(int)
    res = []
    agr = True
    temp = val_high[0]
    last = val_high[0]
    for index,value in enumerate(val_high):
        if value < temp and agr:
            res.append(last)
            agr = False
        elif value > temp:
            last = value
            agr = True
        temp = value
            
    res = _redo(res)

    return res

def _sop(df):
    global nl,rep
    val_Low = df['Low']
    val_o1 = df['Open'].astype(int)
    val_o2 = df['Close'].astype(int)
    sop = []
    agr = True
    temp = val_Low[0]
    last = val_Low[0]
    for index,value in enumerate(val_Low):
        if value > temp and agr:
            sop.append(last)
            agr = False
        elif value < temp:
            last = value
            agr = True
        temp = value

    sop = _redo(sop)
    
    return sop
            
        




df = pd.DataFrame(klines[:, :5],columns=['Date','Open','High','Low','Close'])
#df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = np.round(df['Date'],5)



resistencias = _res(df)
soportes = _sop(df)


x = [df['Date'].iloc[0],df['Date'].iloc[-1]]
xcord = df['Date'].iloc[0]
fig, ax = plt.subplots(figsize=(32, 24))
candlestick_ohlc(ax,df.values , width=10000000, colorup='green', colordown='red')

for a in resistencias:
    ax.plot(x,[a,a],color='red')
    ax.text(xcord, a,str(a), ha="left", va="bottom")
    
for a in soportes:
    ax.plot(x,[a,a],color='green')
    ax.text(xcord, a,str(a), ha="left", va="bottom")

ax.set_title('ETHUSDT')

plt.show()
