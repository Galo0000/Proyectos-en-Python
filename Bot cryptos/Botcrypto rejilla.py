import sys
sys.path.append( 'C:/Repositorios/Python' )
import USERBINANCE
from binance.client import Client
import time
from os import system
import pandas as pd
import numpy as np

from datetime import datetime
import os.path
from websocket import WebSocketApp
import json
import asyncio


class botrack:
    def __init__(self):
        #self.lot_size = self.calculate_lot_size()
        self.client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')
        self.stablecoin = 'USDT'
        self.volatilcoin = 'ETH'
        self.symbolticker = self.volatilcoin + self.stablecoin
        #self.reglocalbuys = pd.read_csv()
        #self.regonlinebuys =
        self.rack = np.empty([1, 1], dtype=float)
        self.price = 0
        self.preice_up = 0
        self.price_down = 0
        self.price_lock = 0
        self.price_range = 100
        self.inv_per_rack = 15
        self.fees = 0.001
        self.real_inv = self.inv_per_rack * (1+self.fees)
        self.minprice = 0
    
    def run(self,ws,msg):
        system('cls')
        tick = json.loads(msg)
        a = float(tick['k']['c'])
        self.price = np.round_(a,decimals = 2, out = None)
        self.price_up = self.price + self.price_range
        self.price_down = self.price - self.price_range
        print(self.price_up)
        print(self.price)
        print(self.price_down)
        print('**************************************************')
   
        for enum, price in enumerate(self.rack):
            if price == self.minprice:
                break
            else:
                print(price)
                if self.price < price and self.price > self.rack[enum+1]:
                    print('*')
                if price < self.price_up and price > self.price:
                    self.price_lock = price
                    print('looooooock',self.price_lock)
                if price < self.price and price > self.price_down:
                    self.price_lock = price
                    print('looooooock',self.price_lock)

                
    def get_rack_list(self):
        hklines = np.array(self.client.get_klines(symbol=self.symbolticker, interval=Client.KLINE_INTERVAL_1MONTH,limit=15)).astype(np.float64)
        maxprice = hklines[:,2].max()
        print(maxprice)
        self.minprice = hklines[:,3].min()
        print(self.minprice)
        temp = maxprice
        if not os.path.isfile('rack.npy'):  
            while temp > self.minprice:
                qty = self.inv_per_rack / self.minprice
                temp -= 300 #((qty * price)*self.fees) - self.real_inv
                self.rack = np.append(self.rack, temp)
           
            #np.save('rack.npy', self.rack)
            print(self.rack)
        else:
            self.rack = np.load('rack.npy', allow_pickle = True)
            
            
            
            
            
    def send_order(self,side,order,qty,price):
        while 1:
            order = self.client.create_order(
                symbol=self.symbolticker,
                side=side,
                type=order,
                timeInForce='TIME_IN_FORCE_GTC',
                quantity=qty,
                price=price,
                newOrderRespType='JSON. ACK')
            
            status = self.client.get_order(
                symbol=self.symbolticker,
                orderId=order["orderId"])
            time.sleep(1)
            if status["status"] == 'NEW':
                break
            else:
                continue
            
    
    #def calculate_lot_size(self,):
    #    q*price = (0.5 + (q*buyprice))/fees
        
        
    def start(self):
        ws = WebSocketApp("wss://stream.binance.com:9443/ws/ethusdt@kline_1m", on_message=self.run)
        ws.run_forever()
  
        
        
bot = botrack()
bot.get_rack_list()
bot.start()