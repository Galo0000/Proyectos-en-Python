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
cercania = 5
basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin
klines = np.array(client.get_klines(symbol=symbolTicker, interval=Client.KLINE_INTERVAL_4HOUR,limit=nl)).astype(np.float64)


def _procerc(lista, d):
    lista.sort()
    promedio = 0
    temp = []
    cercanos = []
    
    for i in lista:
        #temp.append(i)
        for l in lista:
            if i != l:
                if i+d > l > i-d:
                    if l not in temp:
                        temp.append(l)
                else:
                    if sum(temp) != 0 and len(temp) != 0 and len(temp) >= 3:
                        promedio = sum(temp)/len(temp)
                        cercanos.append(int(promedio))
                        promedio = 0
                        temp = []
    
    
    return cercanos

def _res(df):
    val_high = df['High'].astype(int)
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
            
    #for i in range(len(result)):
    #    result[i] = int(result[i] / 10) * 10
    #resultfinal = []
    #for n in result:
    #    if result.count(n) >= 3 and n not in resultfinal:
    #        resultfinal.append(n)
    
    for r in range(rep):
        result = _procerc(result,cercania)
    
    return result

def _sop(df):
    global nl,rep
    val_Low = df['Low'].astype(int)
    res = [0]*nl
    n = 0
    isinf = False
    temp = 0
    result = []
    for value in val_Low:
        if value < temp:
            res[n] = value
            isinf = True
        elif isinf:
            isinf = False
            n +=1
        temp = value
            
    for a in res:
        if a != 0:
            result.append(a)
            
    #for i in range(len(result)):
    #    result[i] = int(result[i] / 10) * 10
    #resultfinal = []
    #for n in result:
    #    if result.count(n) >= 3 and n not in resultfinal:
    #        resultfinal.append(n)
    
    for r in range(rep):
        result = _procerc(result,cercania)
    
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

ax.set_title('Gráfico de velas japonesas')
ax.set_xlabel('Fecha')
ax.set_ylabel('Precio')

plt.show()
