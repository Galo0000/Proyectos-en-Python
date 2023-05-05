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
<<<<<<< HEAD
nl = 50
=======
nl = 100
rep = 1
cercania = 3
>>>>>>> 69a276dca1d4e706ccc92880265bacb2e3ce998a
basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin
klines = np.array(client.get_klines(symbol=symbolTicker, interval=Client.KLINE_INTERVAL_4HOUR ,limit=nl)).astype(np.float64)

def _redo(l):
    #prom = []
    #complete = []
    #for a in l:
    #    temp = []
    #    for b in l:
    #        if b not in complete:
    #            if (int(a/10)*10) == (int(b/10)*10):
    #                temp.append(b)
    #                complete.append(b)
    #    if len(temp) >= 3:
    #        print(temp)
    #        prom.append(int(sum(temp)/len(temp)))
            
    prom = []
    complete = []
    for a in l:
        temp = []
        for b in l:
            if b not in temp:
                inter = np.intersect1d(b, a)
                if inter.size > 2:
                    temp.append(b)
                else:
                    break
        for r in temp:
            arreglo_rango = np.array(r)
            promedio_rango = np.mean(arreglo_rango)
            complete.append(promedio_rango)
        pr
    return complete

def _res(df):
    val_high = df['High'].astype(int)
    val_o1 = df['Open'].astype(int)
    val_o2 = df['Close'].astype(int)
    res = np.zeros(nl, dtype=int)
    n = 0
    isup = False
    temp = 0
    result = np.empty(0)
    for index,value in enumerate(val_high):
        if value > temp:
            res[n] = np.arange(value,max(val_o1[index],val_o2[index]))
            isup = True
        elif isup:
            isup = False
            n +=1
        temp = value
            
    result = result[np.nonzero(result)]
            
    result = _redo(result)

    return result

def _sop(df):
    global nl,rep
    val_Low = df['Low'].astype(int)
    val_o1 = df['Open'].astype(int)
    val_o2 = df['Close'].astype(int)
    res = np.zeros(nl, dtype=int)
    n = 0
    isinf = False
    temp = 0
    result = np.empty(0)
    for index,value in enumerate(val_Low):
        if value < temp:
            res[n] = np.arange(value,min(val_o1[index],val_o2[index]))
            isinf = True
        elif isinf:
            isinf = False
            n +=1
        temp = value
            
    result = result[np.nonzero(result)]
            
    result = _redo(result)
    
    return result
            
        




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
