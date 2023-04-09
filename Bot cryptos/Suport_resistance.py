import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append( 'C:/Repositorios/Python' )
import USERBINANCE
from binance.client import Client

# Crea una instancia del cliente de Binance
client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET)

# Define el par de criptomonedas y el intervalo de tiempo
symbol = 'BTCUSDT'
interval = Client.KLINE_INTERVAL_1DAY

while True:
    df = np.array(client.get_klines(symbol=symbol, interval=interval,limit=100)).astype(np.float64)
    df = df[:,3]
    df = pd.DataFrame(df)
    df.plot(label='High')
    
    pivots =[]
    dates = []
    counter = 0
    lastPivot = 0
    Range = [0,0,0,0,0,0,0,0,0,0]
    daterange = [0,0,0,0,0,0,0,0,0,0]
    
    for i in df:
        currentMax = max(Range , default=0)
        value=round(df.iloc[0,i],2)
        
        Range=Range[1:9]
        Range.append(value)
        daterange=daterange[1:9]
        daterange.append(i)
        
        if currentMax == max(Range , default=0):
            counter+=1
        else:
            counter = 0
        if counter ==  5:
            lastPivot=currentMax
            dateloc =Range.index(lastPivot)
            lastDate = daterange[dateloc]
            pivots.append(lastPivot)
            dates.append(lastDate)
    print()
    #print(str(pivots))
    #print(str(dates))
    timeD = dt.timedelta(days=100)
    
    
    for index in range(len(pivots)):
        print(str(pivots[index])+" :" +str(dates[index]))
        
        plt.plot_date([dates[index],dates[index]+timeD],
            [pivots[index],pivots[index]] , linestyle='-' , linewidth=2, marker=',')
    
    plt.show()