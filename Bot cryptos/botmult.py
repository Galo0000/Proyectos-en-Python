from binance.client import Client
import time
from os import system
import pandas as pd
import talib
import numpy as np
import csv
import sys
from datetime import datetime
from colorama import Fore, Back, Style
import math
import tkinter
import re
import curses
import USERBINANCE


client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')

basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin


def _balance_():
    basecoin_local = float(client.get_asset_balance(basecoin, recvWindow=50000)['free'])
    time.sleep(1)
    tradecoin_local = float(client.get_asset_balance(tradecoin, recvWindow=50000)['free'])
    time.sleep(1)
    balance_local = {'coinbase': basecoin_local,'cointrade': tradecoin_local}
    return balance_local

balance = _balance_()



system("cls")
while 1:
    symbolprices = client.get_all_tickers()
    listtemp = []
    tempconvert = ''
    tempsrt = ''
    convertausdt = 0
    row = 0
    # pares con ADA
    for i in range(0,len(symbolprices)):
        temp = symbolprices[i]
        if temp['symbol'] == 'ETHUSDT':
            pricestart = float(temp['price']) * balance['cointrade']
            break
    scr = curses.initscr()
    for a in range(0,len(symbolprices)):
        temp = symbolprices[a]
        if (temp["symbol"].find('ADA') != -1) and temp["symbol"] != 'ADAUSDT' and temp["symbol"] != 'ADABUSD' and temp["symbol"] != 'ADADOWNUSDT' and temp["symbol"] != 'ADAUPUSDT':
            convertacoin = (balance['cointrade']*0.999)*float(temp['price'])
            # pares con ADA
            # Par de ADA a USDT
            tempconvert = temp["symbol"].strip().lstrip("ADA")
            tempsrt = tempconvert+'USDT'
            for e in range(0,len(symbolprices)):
                temp2 = symbolprices[e]
                if temp2["symbol"].endswith('USDT') == True and tempsrt == temp2["symbol"]:
                    temp3 = symbolprices[e]
                else:
                    continue
            convertausdt = (convertacoin*0.999) * (float(temp3['price']))
            profit = convertausdt - pricestart
            scr.addstr(row,0,temp['symbol']+'     =     '+str(round(float(convertacoin),8))+'    '+tempsrt+' =      '+ str(round(convertausdt,8))+ '      profit     = '+ str(round(float(profit),8)))
            row += 1
    scr.refresh()
    time.sleep(0.5)
sys.exit()
