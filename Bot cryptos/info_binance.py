import USERBINANCE
from binance.client import Client
import pandas as pd
import time
import numpy as np
import talib
from tools.Tools import _truncate_


client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')

basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin





def _roundplaces_():
    symbolinfo = client.get_symbol_info(symbolTicker)
    decimalprice_local = symbolinfo['filters'][0]['tickSize']
    roundprice = (decimalprice_local.find('1'))-1
    decimalqty_local = symbolinfo['filters'][2]['stepSize']
    roundqty = (decimalqty_local.find('1'))-1
    
    roundplaceinfo = {'roundprice':roundprice, 'roundqty':roundqty}
    return roundplaceinfo


def _balance_():
    basecoin_local = float(client.get_asset_balance(basecoin, recvWindow=50000)['free'])
    tradecoin_local = float(client.get_asset_balance(tradecoin, recvWindow=50000)['free'])
    balance_local = {'basecoin': basecoin_local,'tradecoin': tradecoin_local}
    return balance_local


def _trades_(isbuyer):
    quantity_local = 0
    while 1:
        trades_local = client.get_my_trades(symbol = symbolTicker, limit = 10)
        if isbuyer == trades_local[-1]['isBuyer']:
            tradetimems = trades_local[-1]['time']
            tradeid = trades_local[-1]['id']
            tradetimeint = int(tradetimems)
            tradetime = str(pd.to_datetime((tradetimeint - 10800000), unit='ms'))
            tradetime = tradetime[:tradetime.rfind(".")]
            for i in range(0,len(trades_local)):
                if trades_local[i]['time'] == tradetimems:
                    quantity_local += float(trades_local[i]['qty'])#-float(trades_local[i]['commission']))
            break
        else:
            time.sleep(1)
            continue
    lasttradeinfo = {'qty': quantity_local,'price': float(trades_local[-1]['price']),'datetime': tradetime,'id':int(tradeid)}
    return lasttradeinfo






def _indicators_():
    global client
    
    while 1:
        try:
            klines = np.array(client.get_klines(symbol=symbolTicker, interval=Client.KLINE_INTERVAL_1DAY,limit=200)).astype(np.float64)
        except:
            time.sleep(20)
            client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')
            continue

        if len(klines) == 200:
            ### DONCH CHANNELs #######
            #MAX = talib.MAX(klines[:,2], 20)
            #MIN = talib.MIN(klines[:,3], 20)
            #CENTRE = MAX[-1] - MIN[-1]
            ############### EN FASE DE PRUEBA #######################
            rsi_local = talib.RSI(klines[:,4],14)
            rsi_local = rsi_local[~np.isnan(rsi_local)]
            fastk, fastd = talib.STOCH(rsi_local,rsi_local,rsi_local, fastk_period=14, slowk_period=3, slowd_period=3)
            #POSDM_local = talib.PLUS_DM(klines[:,2],klines[:,3],timeperiod=14)
            #NEGDM_local = talib.MINUS_DM(klines[:,2],klines[:,3],timeperiod=14)
            #DX_local = talib.DX(klines[:,2],klines[:,3],klines[:,4],timeperiod=14)
            #SAR_local = talib.SAR(klines[:,2],klines[:,3],acceleration=0.02, maximum=0.2)
            ###############################################################
            #POSDI_local = talib.PLUS_DI(klines[:,2],klines[:,3],klines[:,4],timeperiod=10)
            #NEGDI_local = talib.MINUS_DI(klines[:,2],klines[:,3],klines[:,4],timeperiod=10)
            adx_local = talib.ADX(klines[:,2],klines[:,3],klines[:,4],timeperiod=14)
            #sar_local = talib.SAR(klines[:,2],klines[:,3])
            #macd_local = talib.MACD((klines[:,4]),fastperiod=4, slowperiod=26, signalperiod=9)
            ema4_local = talib.EMA(klines[:,4],timeperiod=4)
            ema9_local = talib.EMA(klines[:,4],timeperiod=9)
            ema18_local = talib.EMA(klines[:,4],timeperiod=18)
            upper,middle,lower = talib.BBANDS(klines[:,4],timeperiod=21)
            close_local = klines[:,4]
            #opentime = klines[:,0]
            ########### tiempo de finalizacion de kline #################
            closems_local = int(klines[-1,6])
            #closetime_local = datetime.fromtimestamp((closems_local/1000))
            closetime_local = str(pd.to_datetime((closems_local- 10800000), unit='ms'))
            closetime_local = closetime_local[:closetime_local.rfind(".")]
            #servertimems_local = int(client.get_server_time()['serverTime'])
            #servertime_local = datetime.fromtimestamp((servertimems_local/1000))
            
            #####################################
            temptotal = {'closeprice': _truncate_(close_local[-1],rounds['roundprice'])
                        ,'closetime': closetime_local
                        #,'servertime': servertime_local
                        ,'BBANDS-upper': _truncate_(upper[-1],rounds['roundprice'])
                        ,'BBANDS-middle': _truncate_(middle[-1],rounds['roundprice'])
                        ,'BBANDS-lower': _truncate_(lower[-1],rounds['roundprice'])
                        #,'DC-MAX': MAX[-1]
                        #,'DC-MIN': MIN[-1]
                        #,'DC-CENTRE': CENTRE
                        #,'tendencia': modelo[0]
                        ,'RSI': _truncate_(rsi_local[-1],2)
                        ,'ADX': adx_local[-1]
                        #,'+DI': POSDI_local[-1]
                        #,'-DI': NEGDI_local[-1]
                        ,'STOCHRSI_fastk': fastk[-1]
                        ,'STOCHRSI_fastd': fastd[-1]
                        #,'+DM': POSDM_local[-1]
                        #,'-DM': NEGDM_local[-1]
                        #,'STOCH_slowk': slowk[-1]
                        #,'STOCH_slowd': slowd[-1]
                        #,'SAR': round(sar_local[-1],rounds['roundprice'])
                        #,'EMA4': round(ema4_local[-1],rounds['roundprice'])
                        #,'EMA9': round(ema9_local[-1],rounds['roundprice'])
                        #,'EMA18': round(ema18_local[-1],rounds['roundprice'])
                        #,'MACD': round(macd_local[-1][-1],4)
                        #,'4flag': flags['4']
                        #,'3flag': flags['3']
                        #,'2flag': flags['2']
                        #,'1flag': flags['1']
                        }
            break
        else:
            time.sleep(10)
            continue

    return temptotal