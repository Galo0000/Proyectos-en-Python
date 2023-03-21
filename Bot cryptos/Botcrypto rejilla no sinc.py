import sys
sys.path.append( 'C:/Repositorios/Python' )
import USERBINANCE
from binance.client import Client
import time
from os import system
import pandas as pd
import numpy as np
import win32api
import win32con
import ntplib
from datetime import datetime
import os.path
import curses as cs
import subprocess

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
        self.rack_diff = 200
        self.price_range = self.rack_diff / 6
        self.inv_per_rack = 15
        self.fees = 0.001
        self.real_inv = self.inv_per_rack * (1+self.fees)
        self.minprice = 0
    
    def run(self):
        n = 4
        self.cs.refresh()
        self.price = float(self.client.get_symbol_ticker(symbol=self.symbolticker)['price'])
        self.price = np.round(self.price,2)
        self.price_up = np.round(self.price + self.price_range,2)
        self.price_down = np.round(self.price - self.price_range,2)
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
        order = self.client.create_order(
            symbol=self.symbolticker,
            side=side,
            type=order,
            timeInForce='TIME_IN_FORCE_GTC',
            quantity=qty,
            price=price)
        
        time.sleep(1)
        if order['status'] == 'FILLED':
            return 'Complete'
        else:
            return 'Failed'

            
    
    #def calculate_lot_size(self,):
    #    q*price = (0.5 + (q*buyprice))/fees
        
    
    def update_time(self):
        # Obtener la hora actual desde el servidor de tiempo
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('time.windows.com')
        ntp_time = datetime.fromtimestamp(response.tx_time)
        
        # Convertir la hora a un formato compatible con Windows
        system_time = ntp_time.strftime('%m/%d/%Y %I:%M:%S %p')
        
        # Establecer la hora del sistema en Windows
        win32api.SetSystemTime(int(ntp_time.year), int(ntp_time.month), int(ntp_time.weekday()), int(ntp_time.day), int(ntp_time.hour), int(ntp_time.minute), int(ntp_time.second), 0)

        print("La hora del sistema ha sido actualizada a:", system_time)

  
        
        
bot = botrack()
bot.get_rack_list()
#n = 0
while True:
    #n+=1
    time.sleep(1)
    bot.run()
