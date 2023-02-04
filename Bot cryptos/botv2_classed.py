import USERBINANCE
from binance.client import Client
import time
import pandas as pd
import sys
import curses
import os.path
#my .py
import tools
import info_binance

def __init__():
    client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')
    basecoin = 'USDT'
    tradecoin = 'ETH'
    symbolTicker = tradecoin + basecoin
    
    
    regprofit = pd.read_excel('regtrades.xlsx', engine='openpyxl' )
    regprofit['Ganancia'] = pd.to_numeric(regprofit['Ganancia'], errors='coerce')
    
    
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
    regbuys['ganancia'] = pd.Series([],dtype='float')
    
    
    
    
    ppbuy = 1.002
    ppsell = 0.998
    rej = []
    pnb = 0.95
    rsimax = 80
    rsimin = 20
    test = False
    generator = False
    stopbuy = False
    klinesave = False
    buyflag = True
    df = None
    ################# GRAFICO ####################
    xvals = []
    yvals = []
    ################# VARIABLES ##################
    minprice = 1700
    maxprice = 4868
    #flags = {'1':'','2':'','3':'','4':''}
    gan = 0
    inv = 0
    prev_basecoin = 0
    prev_tradecoin = 0
    quantity = 0
    balance = 0
    paux = 0
    prev_symbolPrice = 0
    coinbaseini = 0
    profit = 0
    psell = 0
    pbuy = 0
    pbuytime = 0
    indicadores = 0
    inversion = 0
    prevbuy = False
    delay = 0
    testopid = int(4000)
    ids = []
    tempzone = 0
    regprofit = pd.DataFrame(columns=['Fecha y Hora'
                                        ,'Compra'
                                        ,'Venta'
                                        ,'Ganancia'
                                        ,'Balance'
                                        ,'Cantidad'
                                        ,'Moneda base'
                                        ,'Moneda cambio'])

    regprofit = pd.DataFrame({'Fecha y Hora':pd.Series([],dtype='str')
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




        
######################################################################################      
def _zones_():
    global status,indicadores,paux,quantity,prev_symbolPrice,tempzone
    
    status = 'z'
    
    while 1:
        scr.clear()
        indicadores = _indicators_()
        tempdfmin = _valuebuy_('min')
        tempzone = tempdfmin.iloc[0]['buyp'] * pnb
        prev_symbolPrice = indicadores['closeprice']
        paux = _truncate_((indicadores['closeprice'] * ppsell),rounds['roundprice'])
        update_regs()
        _interface_()
        ########## CONDITIONS ##############################################
        tocd = [indicadores['STOCHRSI_fastd'] < 15
                ,indicadores['STOCHRSI_fastk'] < 15
                ,indicadores['RSI'] < 45
                ,indicadores['closeprice'] < indicadores['BBANDS-middle']]
        
        tovd = [indicadores['STOCHRSI_fastd'] > 75
                ,indicadores['STOCHRSI_fastk'] > 75
                ,indicadores['RSI'] > 55]
        
        
        
        if all(tocd):
            paux = _truncate_((indicadores['closeprice'] * ppbuy),rounds['roundprice'])
            if indicadores['closeprice'] < (tempdfmin.iloc[0]['buyp']*pnb) and times > 0 and buyflag == True:
                _dinbuysell_('cd')
                status = 'z'
            continue
        if all(tovd):
            paux = _truncate_((indicadores['closeprice'] * ppsell),rounds['roundprice'])
            if tempdfmin.iloc[0]['ganancia'] > tol:
                _dinbuysell_('vd')
                status = 'z'
            continue
        _timesleep_()
        
        continue
            
        ######################################################################
    

def _dinbuysell_(ope):
    global paux,prev_symbolPrice, status, indicadores, quantity,ids,tempzone
    
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
            ids = _valuebuy_('lstid')   
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
            paux = _truncate_((indicadores['closeprice'] * pp),rounds['roundprice'])
            prev_symbolPrice = indicadores['closeprice']
            
        else:
            _timesleep_()
            continue
        
    

def _order_(order_inputdata):
    global profit,balance,testopid,ids,paux,prev_basecoin,prev_tradecoin,gan,inv
    if order_inputdata['type'] == 'buy':
        if test:
            balance = _testbalance_(balance,order_inputdata['type'],order_inputdata['paux'],order_inputdata['qty'])
            price = order_inputdata['paux']
            qty = order_inputdata['qty']
            time = indicadores['closetime']
            testopid += 1
            _buyslist_('add',testopid,time,_truncate_(price,rounds['roundprice']),_truncate_((qty * fees),rounds['roundqty']))

        if not test:
            orderisbuyer = True
            prev_basecoin = balance['basecoin']
            prev_tradecoin = balance['tradecoin']
            order = client.order_market_buy(
                        symbol=order_inputdata['pair'],
                        quantity=order_inputdata['qty'])
            
            trades = _trades_(orderisbuyer)
            balance = _balance_()
            price = trades['price']
            
            ####### inf real desde balance
            if (balance['tradecoin'] - prev_tradecoin) < 0:
                qty = (balance['tradecoin'] - prev_tradecoin)*(-1)
            else:
                qty = (balance['tradecoin'] - prev_tradecoin)
            if (prev_basecoin - balance['basecoin']) < 0:
                inv = (prev_basecoin - balance['basecoin']) * (-1)
            else:
                inv = (prev_basecoin - balance['basecoin'])
            ###############################################################
                
            time = trades['datetime']
            idorder = trades['id']
            _buyslist_('add',idorder
                       ,time
                       ,price
                       ,_truncate_(qty,rounds['roundqty'])
                       ,_truncate_(inv,rounds['roundprice']))
            
        _regtrades_(time,_truncate_(price,rounds['roundprice'])
                            ,'-','-','-'
                            ,_truncate_(qty,rounds['roundqty'])
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
            _buyslist_('delete',ids,time,price,qty)
            ids = []
        if not test:
            orderisbuyer = False
            prev_basecoin = balance['basecoin']
            prev_tradecoin = balance['tradecoin']
            order = client.order_market_sell(
                        symbol=order_inputdata['pair'],
                        quantity=order_inputdata['qty'])
            
            trades = _trades_(orderisbuyer)
            balance = _balance_()
            if (prev_tradecoin - balance['tradecoin']) < 0:
                qty = (prev_tradecoin - balance['tradecoin'])*(-1)
            else:
                qty = (prev_tradecoin - balance['tradecoin'])
            if (balance['basecoin'] - prev_basecoin) < 0:
                gan = (balance['basecoin'] - prev_basecoin) * (-1)
            else:
                gan = (balance['basecoin'] - prev_basecoin)
            
            if inv == 0.00:
                inv = _valuebuy_('invini')
         
            price = trades['price']
            time = trades['datetime']
            netprofit = _truncate_((gan - inv),rounds['roundprice'])
            profit += netprofit
            _buyslist_('delete',ids,time,price,_truncate_(qty,rounds['roundqty']),_truncate_(inv,rounds['roundprice']))
            ids = []


        _regtrades_(time
                    ,'-'
                    ,_truncate_(price,rounds['roundprice'])
                    ,_truncate_(netprofit,4)
                    ,_truncate_(profit,4)
                    ,_truncate_(qty,rounds['roundqty'])
                    ,balance['basecoin']
                    ,balance['tradecoin'])
    #return order_outputdata



profit = regprofit['Ganancia'].sum()

if len(regbuys) > 0:
    times = times - len(regbuys)
    prevbuy = True
    if test == True:
        tempidmax = regbuys[regbuys['id']==regbuys['id'].max()]
        testopid = tempidmax.iloc[0]['id']

########################################################################################
inversion = 0
scr = curses.initscr()
_zones_()
sys.exit()







        
    

    

    






                
