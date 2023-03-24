from binance.client import Client
import sys
sys.path.append( 'C:/Repositorios/Python' )
import USERBINANCE
#import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation
import time
from os import system
import pandas as pd
import talib
#from talib import stream as stm
import numpy as np
import sys
from datetime import datetime
import curses
#import threading
import os.path

################# CONSTANTES ##################
#### rejilla de precios ######
ppbuy = 1.002
ppsell = 0.998
###############################


pnb = 0.95
tol = 0.1
rsimax = 80
rsimin = 20
test = False
generator = False
klinesave = False
prev_basecoin = 0
prev_tradecoin = 0
balance = 0
paux = 0
prev_symbolPrice = 0
indicadores = 0
maxtimes = 15
times = maxtimes
testopid = int(4000)

interface_input = {'symbolTicker':None
                   ,'closetime':None
                   ,'RSI':None
                   ,'MACD':None
                   ,'BB up':None
                   ,'BB mid':None
                   ,'BB down':None
                   ,'STOCHRSI K':None
                   ,'STOCHRSI D':None
                   ,'ADX':None
                   ,'closeprice':None
                   ,'paux':None
                   ,'totalprofit':None
                   ,'basecoin':None
                   ,'tradecoin':None
                   }

regoperations = pd.DataFrame(columns=['Fecha y Hora'
                                    ,'Compra'
                                    ,'Venta'
                                    ,'Ganancia'
                                    ,'Balance'
                                    ,'Cantidad'
                                    ,'Moneda base'
                                    ,'Moneda cambio'])

regoperations = pd.DataFrame({'Fecha y Hora':pd.Series([],dtype='str')
                   ,'Compra':pd.Series([],dtype='float')
                   ,'Venta':pd.Series([],dtype='float')
                   ,'Ganancia':pd.Series([],dtype='float')
                   ,'Balance':pd.Series([],dtype='float')
                   ,'Cantidad':pd.Series([],dtype='float')
                   ,'Moneda base':pd.Series([],dtype='float')
                   ,'Moneda cambio':pd.Series([],dtype='float')
                   })

savekline = pd.DataFrame(columns=['Date','Open','High','Low','Close','Volume'
                                        ,'EMA4' 
                                        ,'EMA9'
                                        ,'EMA18'
                                        ,'RSI'
                                        ,'STOCHRSIK'
                                        ,'STOCHRSID'
                                        ,'BBUPPER'
                                        ,'BBMIDDLE'
                                        ,'BBLOWER'
                                        ])
savekline.to_csv('realtimeklineeth1h.csv',index = False, mode = 'a')
                                        
#order_inputdata = pd.DataFrame(columns=['type'
#                                        #,'test'
#                                        ,'pair'
#                                        ,'paux'
#                                        ,'qty'])
#order_outputdata = pd.DataFrame(columns=['time'
#                                        ,'buyprice'
#                                        ,'sellprice'
#                                        ,'profit'
#                                        ,'balance'
#                                        ,'qty'
#                                        ,'basecoin'
#                                        ,'tradecoin'])
#operation_inputdata = pd.DataFrame(columns=['operation'
#                                             ,'prevprice'
#                                             ,'paux'])
#################################################
######### configracion segun par ###########
def _roundplaces_():
    symbolinfo = client.get_symbol_info(symbolTicker)
    decimalprice_local = symbolinfo['filters'][0]['tickSize']
    roundprice = (decimalprice_local.find('1'))-1
    
    step_size = None
    for f in symbolinfo['filters']:
        if f['filterType'] == 'LOT_SIZE':
            step_size = f['stepSize']
            break
    roundqty = (step_size.find('1'))-1
    
    roundplaceinfo = {'roundprice':roundprice, 'roundqty':roundqty}
    return roundplaceinfo
############################################  DEFS EN DESARROLLO #################################

def update_regs():
    global regbuys
    
    for a in range(len(regbuys)):
        try:
            regbuys.at[a,'ganancia'] = _trc((((regbuys.iloc[a]['qty']*paux)*fees)-regbuys.iloc[a]['inversion']),2)
        except ValueError:
            pass


def _valuebuy_(value):
    result = 0
    
    if value == 'lstid':
        templst = []
        for a in range(len(regbuys)):
            if regbuys.iloc[a]['ganancia'] > tol:
                templst.append(regbuys.iloc[a]['id'])
        result = templst
        
    if value == 'max':
        result = regbuys[regbuys['buyp']==regbuys['buyp'].max()]
    elif value == 'min':
        result = regbuys[regbuys['buyp']==regbuys['buyp'].min()]
    elif value == 'full':
        result = regbuys
    elif value == 'sumqty':
        for a in range(len(regbuys)):
            result += regbuys.iloc[a]['qty']
    elif value == 'invini':
        for t in range(len(regbuys)): 
            if regbuys.iloc[t]['ganancia'] > tol:
                result += regbuys.iloc[t]['inversion']
    return result
    

def _buyslist_(addordelete,idbuy,date,buyp,qty,inv):
    global times, regbuys
    if test:
        file = "testbuylist.csv"
    if not test:
        file = "buylist.csv"
        
    if addordelete == 'add':
        df = pd.DataFrame({'id': [idbuy],'date': [date],'buyp': [buyp],'qty': [qty],'inversion':[inv]})
        df.to_csv(file,index = False, header = False, mode = 'a')
        df = pd.DataFrame({'id': [idbuy],'date': [date],'buyp': [buyp],'qty': [qty],'inversion':[inv],'ganancia':[(qty*paux)-(qty*buyp)]})
        regbuys = regbuys.append(df,ignore_index=True)
        times = maxtimes - len(regbuys)
    if addordelete == 'delete':
        temp = pd.read_csv(file)
        for a in range(len(idbuy)):
            try:
                temp = temp.drop(temp[(temp['id']==idbuy[a])].index)
                regbuys = regbuys.drop(regbuys[(regbuys['id']==idbuy[a])].index)
            except IndexError:
                pass
                    
        temp.to_csv(file,index = False)
        times = maxtimes - len(regbuys)
        
######################################################################################      
def _zones_():
    global status,indicadores,paux,prev_symbolPrice
    
    status = 'z'
    
    while 1:
        scr.clear()
        indicadores = _indicators_()
        tempdfmin = _valuebuy_('min')
        prev_symbolPrice = indicadores['closeprice']
        paux = _trc((indicadores['closeprice'] * ppsell),rounds['roundprice'])
        update_regs()
        _interface_()
        ########## CONDITIONS ##############################################
        tocd = [indicadores['STOCHRSI_fastd'] < 50
                ,indicadores['STOCHRSI_fastk'] < 50
                ,indicadores['RSI'] < 50
                ,indicadores['MACD'] < 0
                ,indicadores['closeprice'] < indicadores['BBANDS-middle']]
        
        tovd = [indicadores['STOCHRSI_fastd'] > 50
                ,indicadores['STOCHRSI_fastk'] > 50
                ,indicadores['RSI'] > 50
                ,indicadores['MACD'] > 0]
        
        if all(tocd):
            paux = _trc((indicadores['closeprice'] * ppbuy),rounds['roundprice'])
            if indicadores['closeprice'] < (tempdfmin.iloc[0]['buyp']*pnb) and times > 0:
                _dinbuysell_('cd')
                status = 'z'
            continue
        elif all(tovd):
            paux = _trc((indicadores['closeprice'] * ppsell),rounds['roundprice'])
            if tempdfmin.iloc[0]['ganancia'] > tol:
                _dinbuysell_('vd')
                status = 'z'
            continue
        _timesleep_()
        continue
            
        ######################################################################
    

def _dinbuysell_(ope):
    global paux,prev_symbolPrice, status, indicadores
    
    status = ope
    
    while 1:
        scr.clear()
        indicadores = _indicators_()
        update_regs()
        quantity = _quantity_()
        _interface_()
        
        if ope == 'cd':
            pp = ppbuy
            op = 'buy'
            b = [indicadores['closeprice'] < prev_symbolPrice]
            a = [indicadores['closeprice'] > paux]
                
        if ope == 'vd':
            tempdfmin = _valuebuy_('min')
            pp = ppsell
            op = 'sell'
            b = [indicadores['closeprice'] > prev_symbolPrice]
            a = [indicadores['closeprice'] < paux
                 ,tempdfmin.iloc[0]['ganancia'] > tol]
        
        if all(a):
            order_inputdata = {'type':op
                               ,'pair':symbolTicker
                               ,'paux':paux
                               ,'qty':quantity}
            _order_(order_inputdata)
            _timesleep_()
            break
        
        
        
        if status =='vd':
            tempzone = (tempdfmin.iloc[0]['buyp'] * pnb)
            if indicadores['closeprice'] < tempdfmin.iloc[0]['buyp'] and indicadores['closeprice'] > tempzone:
                break
            #if indicadores['closeprice'] < tempzone and times > 0:
            #    _nextbuy_()
            #    continue
        if all(b):
            paux = _trc((indicadores['closeprice'] * pp),rounds['roundprice'])
            prev_symbolPrice = indicadores['closeprice']
            
        else:
            _timesleep_()
            continue
        
    

def _order_(order_inputdata):
    global balance,testopid,paux,prev_basecoin,prev_tradecoin
    profit = 0
    gan = 0
    if order_inputdata['type'] == 'buy':
        if test:
            balance = _testbalance_(balance,order_inputdata['type'],order_inputdata['paux'],order_inputdata['qty'])
            price = order_inputdata['paux']
            qty = order_inputdata['qty']
            time = indicadores['closetime']
            testopid += 1
            _buyslist_('add',testopid,time,_trc(price,rounds['roundprice']),_trc((qty * fees),rounds['roundqty']))

        if not test:
            orderisbuyer = True
            prev_basecoin = balance['basecoin']
            prev_tradecoin = balance['tradecoin']
            client.order_market_buy(
                symbol=order_inputdata['pair'],
                quantity=order_inputdata['qty'],)
            
            trades = _trades_(orderisbuyer)
            balance = _balance_()
            price = trades['price']
            
 
            qty = abs(balance['tradecoin'] - prev_tradecoin)
            inv = abs(prev_basecoin - balance['basecoin'])
            ###############################################################
                
            time = trades['datetime']
            idorder = trades['id']
            _buyslist_('add',idorder
                       ,time
                       ,price
                       ,_trc(qty,rounds['roundqty'])
                       ,_trc(inv,rounds['roundprice']))
            
        _regtrades_(time,_trc(price,rounds['roundprice'])
                            ,0,0,0
                            ,_trc(qty,rounds['roundqty'])
                            ,balance['basecoin']
                            ,balance['tradecoin'])

    if order_inputdata['type'] == 'sell':
        if test:
            balance = _testbalance_(balance,order_inputdata['type'],order_inputdata['paux'],order_inputdata['qty'])
            price = order_inputdata['paux']
            time = indicadores['closetime']
            qty = order_inputdata['qty']
            netprofit =((qty*fees)*price) - _valuebuy_('invini')
            profit += netprofit
            _buyslist_('delete',_valuebuy_('lstid'),time,price,qty)
        if not test:
            orderisbuyer = False
            prev_basecoin = balance['basecoin']
            prev_tradecoin = balance['tradecoin']
            client.order_market_sell(
                symbol=order_inputdata['pair'],
                quantity=order_inputdata['qty'])
            
            trades = _trades_(orderisbuyer)
            balance = _balance_()
            
            qty = abs(prev_tradecoin - balance['tradecoin'])
            gan = abs(balance['basecoin'] - prev_basecoin)
            
            inv = _valuebuy_('invini')
         
            price = trades['price']
            time = trades['datetime']
            netprofit = _trc((gan - inv),rounds['roundprice'])
            profit += netprofit
            _buyslist_('delete',_valuebuy_('lstid'),time,price,_trc(qty,rounds['roundqty']),_trc(inv,rounds['roundprice']))


        _regtrades_(time
                    ,0
                    ,_trc(price,rounds['roundprice'])
                    ,_trc(netprofit,4)
                    ,_trc(profit,4)
                    ,_trc(qty,rounds['roundqty'])
                    ,balance['basecoin']
                    ,balance['tradecoin'])


###################################################################################################

def _trc(num,n):
    i = int(num * (10**n))/(10**n)
    return float(i)

def _regtrades_(date,bprice,sprice,profit,balance,qty,basecoin,tradecoin):
    global regoperations
        
    tempregprofit = pd.DataFrame({'Fecha y Hora': [date]
                                ,'Compra': [bprice]
                                ,'Venta': [sprice]
                                ,'Ganancia':[profit]
                                ,'Balance':[balance]
                                ,'Cantidad':[qty]
                                ,'Moneda base':[basecoin]
                                ,'Moneda cambio':[tradecoin]
                                })
    regoperations = regoperations.append(tempregprofit,ignore_index = True)
    regoperations.to_excel('regtrades.xlsx', sheet_name='regtrades', index=False)


def _interface_():
    row = 0
    if status == 'z':
        x = 'ESPERANDO CONDICIONES'
    if status == 'cd':
        x = 'COMPRA DINAMICA'
    if status == 'vd':
        x = 'VENTA DINAMICA'
    scr.addstr(row,0,str(symbolTicker))
    row += 1
    scr.addstr(row,0,'Proxima vela :'+str(indicadores['closetime']))
    row += 1
    scr.addstr(row,0,x)
    row += 1
    scr.addstr(row,0,str(regbuys))
    row += maxtimes + 1
    scr.addstr(row,0,"*******************************")
    row += 1
    scr.addstr(row,0,'Compras disponibles : '+str(times)+'/'+str(maxtimes))
    row += 1
    scr.addstr(row,0,' RSI = '+str(indicadores['RSI']))
    row += 1
    scr.addstr(row,0,' MACD = '+str(indicadores['MACD']))
    row += 1
    scr.addstr(row,0,' BB up   = '+str(_trc(indicadores['BBANDS-upper'],rounds['roundprice'])))
    row += 1
    scr.addstr(row,0,' BB mid  = '+str(_trc(indicadores['BBANDS-middle'],rounds['roundprice'])))
    row += 1
    scr.addstr(row,0,' BB down = '+str(_trc(indicadores['BBANDS-lower'],rounds['roundprice'])))
    row += 1
    scr.addstr(row,0,' STOCHRSI K = '+str(_trc(indicadores['STOCHRSI_fastk'],2)))
    row += 1
    scr.addstr(row,0,' STOCHRSI D = '+str(_trc(indicadores['STOCHRSI_fastd'],2)))
    row += 1
    scr.addstr(row,0,' ADX = '+str(_trc(indicadores['ADX'],2)))
    row += 1
    #scr.addstr(row,0,' flag 4      = '+indicadores['4flag'])
    #row += 1
    #scr.addstr(row,0,' flag 3      = '+indicadores['3flag'])
    #row += 1
    #scr.addstr(row,0,' flag 2      = '+indicadores['2flag'])
    #row += 1
    #scr.addstr(row,0,' flag actual = '+indicadores['1flag'])
    #row += 1
    scr.addstr(row,0,"*******************************")
    row += 1
    scr.addstr(row,0," Precio                     " + str(indicadores['closeprice']))
    row += 1
    if status == 'cd' or status == 'vd':
        scr.addstr(row,0," Precio seteado actual    " + str(_trc(paux,rounds['roundprice'])))
        row += 1
    scr.addstr(row,0," Precio minimo de compra    " + str(_trc((_valuebuy_('min').iloc[0]['buyp'] * pnb),rounds['roundprice'])))
    row += 1
    scr.addstr(row,0,"*******************************")
    row += 1
    if status == 'z':
        scr.addstr(row,0,"Esperando ")
        row += 1
    scr.addstr(row,0," Ganancia Total          = " + str(_trc(regoperations['Ganancia'].sum(),8)))
    row += 1
    scr.addstr(row,0,"********************************")
    row += 1
    scr.addstr(row,0,str(basecoin) +  " total               = " + str(balance['basecoin']))
    row += 1
    scr.addstr(row,0,str(tradecoin) + " total                = " + str(f"{balance['tradecoin']:.8f}"))
    row += 1
    scr.addstr(row,0,"********* registro de trades **********")
    row += 1
    try:
        scr.addstr(row,0,str(regoperations))
    except curses.error:
        pass
    scr.refresh()
    
    

##################### GENERATOR!!! #################################
def _generator_():
    for i in range(200,len(klines)-200):
        temp = []
        for j in range(i, 200 + i):
            temp.append(klines[j])
        yield temp
 
def _testbalance_(balances, typeorder, price, qty):
    if typeorder == 'sell':
        balances['basecoin'] += price * (qty * fees)
        balances['tradecoin'] -= qty
        return balances
    
    if typeorder == 'buy':
        balances['tradecoin'] += qty * fees
        balances['basecoin'] -= qty * price
        return balances
    
################ Obtiene el balance de las coins en monedero#################
def _balance_():
    basecoin_local = float(client.get_asset_balance(basecoin, recvWindow=50000)['free'])
    time.sleep(1)
    tradecoin_local = float(client.get_asset_balance(tradecoin, recvWindow=50000)['free'])
    time.sleep(1)
    balance_local = {'basecoin': _trc(basecoin_local,2),'tradecoin': tradecoin_local}
    return balance_local

####################### Obtiene indicadores con libreria talib y numpy ######################################
def _indicators_():
    global client
    
    while 1:
        if generator:
            try:
                klines = np.array(next(g)).astype(np.float64)
            except:
                system("cls")
                print(str(profit))
                sys.exit()
        else:
            try:
                klines = np.array(client.get_klines(symbol=symbolTicker, interval=Client.KLINE_INTERVAL_4HOUR,limit=200)).astype(np.float64)
            except:
                time.sleep(20)
                client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')
                continue

        if len(klines) == 200:
            #for a in range(1,5):
            #    if klines[len(klines)-a,4] > klines[len(klines)-a,1]:
            #        flags[str(a)] = 'green'
            #    else:
            #        flags[str(a)] = 'red  '
            ### DONCH CHANNELs #######
            #MAX = talib.MAX(klines[:,2], 20)
            #MIN = talib.MIN(klines[:,3], 20)
            #CENTRE = MAX[-1] - MIN[-1]
            ############### EN FASE DE PRUEBA #######################
            #_realtimeklines_(klines[-1])
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
            macd_local = talib.MACD((klines[:,4]),fastperiod=12, slowperiod=26, signalperiod=9)
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
            temptotal = {'closeprice': _trc(close_local[-1],rounds['roundprice'])
                        ,'closetime': closetime_local
                        #,'servertime': servertime_local
                        ,'BBANDS-upper': _trc(upper[-1],rounds['roundprice'])
                        ,'BBANDS-middle': _trc(middle[-1],rounds['roundprice'])
                        ,'BBANDS-lower': _trc(lower[-1],rounds['roundprice'])
                        #,'DC-MAX': MAX[-1]
                        #,'DC-MIN': MIN[-1]
                        #,'DC-CENTRE': CENTRE
                        #,'tendencia': modelo[0]
                        ,'RSI': _trc(rsi_local[-1],2)
                        ,'ADX': adx_local[-1]
                        #,'+DI': POSDI_local[-1]
                        #,'-DI': NEGDI_local[-1]
                        ,'STOCHRSI_fastk': _trc(fastk[-1],0)
                        ,'STOCHRSI_fastd': _trc(fastd[-1],0)
                        #,'+DM': POSDM_local[-1]
                        #,'-DM': NEGDM_local[-1]
                        #,'STOCH_slowk': slowk[-1]
                        #,'STOCH_slowd': slowd[-1]
                        #,'SAR': _truncate_(sar_local[-1],rounds['roundprice'])
                        #,'EMA4': _truncate_(ema4_local[-1],rounds['roundprice'])
                        #,'EMA9': _truncate_(ema9_local[-1],rounds['roundprice'])
                        #,'EMA18': _truncate_(ema18_local[-1],rounds['roundprice'])
                        ,'MACD': _trc(macd_local[-1][-1],0)
                        #,'4flag': flags['4']
                        #,'3flag': flags['3']
                        #,'2flag': flags['2']
                        #,'1flag': flags['1']
                        }
            if klinesave == True:
                timenow = str(datetime.now())
                df = pd.DataFrame({'Date': [timenow[:timenow.rfind(".")]]
                                      ,'Open': [_trc(klines[-1,1],rounds['roundprice'])]
                                      ,'High': [_trc(klines[-1,2],rounds['roundprice'])]
                                      ,'Low': [_trc(klines[-1,3],rounds['roundprice'])]
                                      ,'Close': [_trc(klines[-1,4],rounds['roundprice'])]
                                      ,'Volume': [_trc(klines[-1,5],2)]
                                      ,'EMA4': [_trc(ema4_local[-1],rounds['roundprice'])]
                                      ,'EMA9': [_trc(ema9_local[-1],rounds['roundprice'])]
                                      ,'EMA18': [_trc(ema18_local[-1],rounds['roundprice'])]
                                      ,'RSI': [_trc(rsi_local[-1],0)]
                                      ,'STOCHRSIK': [_trc(fastk[-1],0)]
                                      ,'STOCHRSID': [_trc(fastd[-1],0)]
                                      ,'BBUPPER': [_trc(upper[-1],rounds['roundprice'])]
                                      ,'BBMIDDLE': [_trc(middle[-1],rounds['roundprice'])]
                                      ,'BBLOWER': [_trc(lower[-1],rounds['roundprice'])]
                                      })
                df.to_csv('realtimeklineeth1h.csv', index=False, header=False, mode='a')
            break
        else:
            time.sleep(10)
            continue

    return temptotal
############### funcion de tiempos ##################
def _timesleep_():
    if generator:
        timepref = 0
    if not generator:
        timepref = 1.5
    time.sleep(timepref)
################### Obtiene informacion de trades #####################
def _trades_(isbuyer):
    while 1:
        trades_local = client.get_my_trades(symbol = symbolTicker, limit = 10)
        if isbuyer == trades_local[-1]['isBuyer']:
            tradetimems = trades_local[-1]['time']
            tradeid = trades_local[-1]['id']
            tradetimeint = int(tradetimems)
            tradetime = str(pd.to_datetime((tradetimeint - 10800000), unit='ms'))
            tradetime = tradetime[:tradetime.rfind(".")]
            break
        else:
            time.sleep(1)
            continue
    lasttradeinfo = {'price': float(trades_local[-1]['price']),'datetime': tradetime,'id':int(tradeid)}
    return lasttradeinfo

def _quantity_():
    quantity = 0
    if status == 'cd':
        tempqty = (int(balance['basecoin'])/times)/paux
        quantity = _trc(tempqty,rounds['roundqty'])

    if status == 'vd':
        tempq = 0
        for t in range(len(regbuys)): 
            if regbuys.iloc[t]['ganancia'] > tol:
                tempq += regbuys.iloc[t]['qty']
        if tempq == 0:
            tempdfmin = _valuebuy_('min')
            tempq = tempdfmin.iloc[0]['qty']
                    
        quantity = _trc(tempq,rounds['roundqty'])
    return quantity
        


########################### INICIO DE PROGRAMA #######################
if os.path.isfile('acta.csv'):
    os.remove('acta.csv')
#    os.remove('testbuylist.csv')
#    os.remove('regtrades.xlsx')


if not os.path.isfile('regtrades.xlsx'):
    df = pd.DataFrame(columns=['Fecha y Hora','Compra','Venta','Ganancia','Balance','Cantidad','Moneda base','Moneda cambio'])
    df.to_excel('regtrades.xlsx',sheet_name='regtrades', index=False)
else:   
    regoperations = pd.read_excel('regtrades.xlsx', engine='openpyxl' )
    regoperations['Ganancia'] = pd.to_numeric(regoperations['Ganancia'], errors='ignore')

client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')

basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin

###############################################



if tradecoin == 'BNB':
    fees = 0.99925
else:
    fees = 0.999

if generator:
    klines = client.get_historical_klines(symbolTicker,Client.KLINE_INTERVAL_15MINUTE, '4 week ago')
    g = _generator_()
rounds = _roundplaces_()
balance = _balance_()
indicadores = _indicators_()

#########################   MENU ######################################


################################ trabajando ###################################

if test:
    file = "testbuylist.csv"
if not test:
    file = "buylist.csv"
    
if not os.path.isfile(file):
    df = pd.DataFrame({'id':pd.Series([],dtype='int')
                       ,'date':pd.Series([],dtype='str')
                       ,'buyp':pd.Series([],dtype='float')
                       ,'qty':pd.Series([],dtype='float')
                       ,'inversion':pd.Series([],dtype='float')})
    df.set_index('id', inplace=True)
    df.to_csv(file)
    

regbuys = pd.read_csv(file)
#regbuys.to_excel('regbuys.xlsx', sheet_name='regbuys', index=False)

regbuys['ganancia'] = pd.Series([],dtype='float')


profit = regoperations['Ganancia'].sum()

if len(regbuys) > 0:
    times = times - len(regbuys)
    if test == True:
        tempidmax = regbuys[regbuys['id']==regbuys['id'].max()]
        testopid = tempidmax.iloc[0]['id']

########################################################################################
scr = curses.initscr()
_zones_()
sys.exit()