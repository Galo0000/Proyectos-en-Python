from binance.client import Client
from binance.enums import HistoricalKlinesType
import USERBINANCE
import pandas as pd
import numpy as np
import talib as tb
import sys

client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')
n = 1.5

def _add_(openk,highk,lowk,tempk):
    dft = pd.DataFrame({'Open': [openk],'High': [highk],'Low': [lowk],'Close': [tempk]})
    dff = dff.append(dft,ignore_index=True)


def _dfklines_():
    symbolTicker = 'ETHUSDT'
    temp = 0
    roundind = 2

    symbolinfo = client.get_symbol_info(symbolTicker)
    decimalprice_local = symbolinfo['filters'][0]['tickSize']
    roundvalue = (decimalprice_local.find('1'))-1
    

    dff = pd.DataFrame(columns=['Date','Open','High','Low','Close','Volume','EMA4','EMA9','EMA18','RSI','STOCHRSIK','STOCHRSID'
                                                                                            ,'MACDs'
                                                                                            ,'MACDh'
                                                                                            ,'MACD'
                                                                                            ,'BBUPPER'
                                                                                            ,'BBMIDDLE'
                                                                                            ,'BBLOWER'
                                                                                            ,'ADX'
                                                                                            ])
    

    dff.to_csv((symbolTicker+'4hour6monthn.csv'), mode = 'a')

    klines = np.array(client.get_historical_klines(symbolTicker,Client.KLINE_INTERVAL_4HOUR,'6 month ago', klines_type=HistoricalKlinesType.SPOT)).astype(np.float64)
    
    for i in range(0,len(klines)):
        openk = klines.iloc[i]['Open']
        closek = klines.iloc[i]['Close']
        highk = klines.iloc[i]['High']
        lowk = klines.iloc[i]['Low']
        if openk > closek:
            flag = 'green'
        else:
            flag = 'red'
        _add_(openk,highk,lowk,closek)
        temp = openk
        if flag == 'green':
            while 1:
                temp -= n
                if temp < lowk:
                    temp = lowk
                    _add_(openk,highk,lowk,temp)
                    break
                else:
                    _add_(openk,highk,lowk,temp)
                    continue
            while 1:
                temp += n
                if temp > highk:
                    temp = highk
                    _add_(openk,highk,lowk,temp)
                    break
                else:
                    _add_(openk,highk,lowk,temp)
                    continue
            while 1:
                temp -= n
                if temp < closek:
                    temp = closek
                    _add_(openk,highk,lowk,temp)
                    break
                else:
                    _add_(openk,highk,lowk,temp)
                    continue
            
        if flag == 'red':
            while 1:
                temp += n
                if temp > highk:
                    temp = highk
                    _add_(openk,highk,lowk,temp)
                    break
                else:
                    _add_(openk,highk,lowk,temp)
                    continue
            while 1:
                temp -= n
                if temp < lowk:
                    temp = lowk
                    _add_(openk,highk,lowk,temp)
                    break
                else:
                    _add_(openk,highk,lowk,temp)
                    continue
            while 1:
                temp += n
                if temp > closek:
                    temp = closek
                    _add_(openk,highk,lowk,temp)
                    break
                else:
                    _add_(openk,highk,lowk,temp)
                    continue
                
                
    
    dateval = pd.to_datetime((klines[:,0] - 10800000), unit='ms')
    #dateval = dateval[:dateval.rfind(".")]
    df['Date'] = dateval
    df['Open'] = np.round(klines[:,1],roundvalue)
    df['High'] = np.round(klines[:,2],roundvalue)
    df['Low'] = np.round(klines[:,3],roundvalue)
    df['Close'] = np.round(klines[:,4],roundvalue)
    df['Volume'] = np.round(klines[:,5],roundind)
    df['EMA4'] = np.round(tb.EMA(klines[:,4],timeperiod=4),roundvalue)
    df['EMA9'] = np.round(tb.EMA(klines[:,4],timeperiod=9),roundvalue)
    df['EMA18'] = np.round(tb.EMA(klines[:,4],timeperiod=18),roundvalue)  
    df['RSI'] = np.round(tb.RSI(klines[:,4],14),0)
    for i in range(0,len(df)):
        if df.iloc[i]['RSI'] < 0:
            df.iloc[i]['RSI'] = 0
    fastk, fastd = tb.STOCH(df['RSI'],df['RSI'],df['RSI'], fastk_period=14, slowk_period=3, slowd_period=3)
    macd,macds,macdh = tb.MACD((klines[:,4]),fastperiod=12, slowperiod=26, signalperiod=9)
    upper,middle,lower = tb.BBANDS(klines[:,4],timeperiod=21)
    df['STOCHRSIK'] = np.round(fastk,0)
    df['STOCHRSID'] = np.round(fastd,0)
    df['MACDs'] = np.round(macds,0)
    df['MACDh'] = np.round(macdh,0)
    df['MACD'] = np.round(macd,0)
    df['BBUPPER'] = np.round(upper,roundvalue)
    df['BBMIDDLE'] = np.round(middle,roundvalue)
    df['BBLOWER'] = np.round(lower,roundvalue)
    #df['MA200'] = np.round(tb.MA(klines[:,4],timeperiod=200),roundvalue)
    df['ADX'] = np.round(tb.ADX(klines[:,2],klines[:,3],klines[:,4],timeperiod=14),roundind)
        
    df.to_csv((symbolTicker+'4hour6monthn.csv'), index = False, header = False, mode = 'a')
    sys.exit()


_dfklines_()
