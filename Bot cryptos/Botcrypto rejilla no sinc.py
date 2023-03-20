import sys
sys.path.append( 'C:/Repositorios/Python' )
import USERBINANCE
from binance.client import Client
import time
from os import system
import pandas as pd
import numpy as np
import win32api as w32
from datetime import datetime
import os.path
import curses as cs

class botrack:
    def __init__(self):
        self.cs = cs.initscr()
        #cs.start_color()
        #cs.init_pair(1, self.cs.COLOR_YELLOW, self.cs.COLOR_BLACK)
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
        self.rack_diff = 50
        self.price_range = self.rack_diff / 4
        self.inv_per_rack = 15
        self.fees = 0.001
        self.real_inv = self.inv_per_rack * (1+self.fees)
        self.minprice = 0
    
    def run(self):
        n = 4
        self.cs.refresh()
        self.price = float(self.client.get_symbol_ticker(symbol=self.symbolticker)['price'])
        self.price = np.round(self.price,2)
        self.price_up = self.price + self.price_range
        self.price_down = self.price - self.price_range
        self.cs.addstr(0,0,str(self.price_up))
        self.cs.addstr(1,0,str(self.price))
        self.cs.addstr(2,0,str(self.price_down))
        self.cs.addstr(3,0,'**************************************************')
   
        for enum, price in enumerate(self.rack):
            if price == self.minprice:
                break
            else:
                try:
                    n+=1
                    self.cs.addstr(n,0,str(price)+'                           ')
                    if price > self.price > self.rack[enum+1]:
                        n+=1
                        self.cs.addstr(n,0,'   *                         ')
                    if self.price_up > price > self.price:
                        n+=1
                        self.price_lock = price
                        self.cs.addstr(n,0,'looooooock to sell  '+str(self.price_lock),)
                    if self.price > price > self.price_down:
                        n+=1
                        self.price_lock = price
                        self.cs.addstr(n,0,'looooooock to buy '+str(self.price_lock))
                except cs.error:
                    pass

                
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
                temp -= self.rack_diff #((qty * price)*self.fees) - self.real_inv
                temp = np.trunc(temp)
                self.rack = np.append(self.rack,temp)
           
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
        
    
    def update_time(self):
        now = w32.getsystem
        seconds = now // 10000000 - 11644473600

        # Actualiza la hora del sistema utilizando SetSystemTime()
        w32.SetSystemTime(
        seconds)

  
        
        
bot = botrack()
bot.get_rack_list()
#n = 0
while True:
    #n+=1
    time.sleep(1)
    bot.run()
    #if n == 100:
    #    bot.update_time()
    #    n = 0