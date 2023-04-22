import sys
sys.path.append( 'C:/Repositorios/Python' )
sys.path.append( 'H:\Repositorios\Python no github\Bot cryptos' )
import USERBINANCE
from binance.client import Client
import time
import pandas as pd
import numpy as np
import win32api
#import ntplib
from datetime import datetime
import os.path
import curses as cs

class botrack:
    def __init__(self):
        # INTERFAZ
        self.cs = cs.initscr()
        #self.lot_size = self.calculate_lot_size()
        # BINACE LOGIN
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
        self.rack_diff = 25
        self.price_range = self.rack_diff / 6
        self.inv_per_rack = 15
        self.fees = 0.001
        self.real_inv = self.inv_per_rack * (1+self.fees)
        self.n = 0
        self.prices = []
        self.dates = []
        self.priceround = self._roundplaces()[0]
        self.qtyround = self._roundplaces()[1]
    
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
            if enum == 0:
                continue
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
                self.cs.refresh()

                
    def get_rack_list(self):
        hklines = np.array(self.client.get_klines(symbol=self.symbolticker, interval=Client.KLINE_INTERVAL_1MONTH,limit=6)).astype(np.float64)
        maxprice = hklines[:,2].max()
        print(maxprice)
        minprice = hklines[:,3].min()
        print(minprice)
        temp = maxprice
        if not os.path.isfile('rack.npy'):  
            while temp > minprice:
                qty = self.inv_per_rack / minprice
                temp -= self.rack_diff #((qty * price)*self.fees) - self.real_inv
                temp = np.trunc(temp)
                self.rack = np.append(self.rack,temp)
           
            np.save('rack.npy', self.rack)
            print(self.rack)
        else:
            self.rack = np.load('rack.npy', allow_pickle = True)
            
            
    def send_order(self,side,order,qty,price):
        result = self.client.create_order(
                symbol=self.symbolticker,
                side=side,
                type=order,
                timeInForce='GTC',
                quantity=qty,
                price=price)
        order = result

        #with open('order_id.txt', 'a') as f:
        #    f.write(str(order_id)+ "\n")
        
        t = str(pd.to_datetime((order['transactTime'] - 10800000), unit='ms'))
        t = t[:t.rfind(".")]
        p = self._trc(float(order['price']),self.priceround)
        q = self._trc(float(order['origQty']),self.qtyround)
        i = self._trc(qty * price,2)
        
        self._regtradeop(True,order['orderId'],t,p,q,i)

    def cancel_order(self,order_id):
        cancelled_order = self.client.cancel_order(
            symbol=self.symbolticker,
            orderId=order_id)
            
    
    #def calculate_lot_size(self,):
    #    q*price = (0.5 + (q*buyprice))/fees
        
    
    #def update_time(self):
    #    # Obtener la hora actual desde el servidor de tiempo
    #    ntp_client = ntplib.NTPClient()
    #    response = ntp_client.request('time.windows.com')
    #    ntp_time = datetime.fromtimestamp(response.tx_time)
        
        # Convertir la hora a un formato compatible con Windows
    #    system_time = ntp_time.strftime('%m/%d/%Y %I:%M:%S %p')
        
        # Establecer la hora del sistema en Windows
    #    win32api.SetSystemTime(int(ntp_time.year), int(ntp_time.month), int(ntp_time.weekday()), int(ntp_time.day), int(ntp_time.hour), int(ntp_time.minute), int(ntp_time.second), 0)

    #    print("La hora del sistema ha sido actualizada a:", system_time)

  
    def _regtrade(self):
        df = pd.DataFrame(columns=['id_orden', 'Fecha y Hora', 'Precio', 'Cantidad', 'Inversion'])
        df.to_csv('reg_trades.csv', index=False)
        return df
        
    def _regtradeop(self,append,idorder,date,price,qty,inv):
        
        file = 'reg_trades.csv'
        
        if append:
            df = pd.DataFrame({'id_orden': [idorder],'Fecha y Hora': [date],'Precio': [price],'Cantidad': [qty],'inversion':[inv]})
            ###### FALTA
            with open(file, mode='a', newline='') as file:
                df.to_csv(file, header=(not file.tell()), index=False)
            
        if not append:
            df = pd.read_csv(file)
            df = df.drop(index=df[df['id_orden'] == idorder].index)
            df.to_csv(file,index = False)
            
    def _roundplaces(self):
        symbolinfo = self.client.get_symbol_info(self.symbolticker)
        decimalprice_local = symbolinfo['filters'][0]['tickSize']
        roundprice = (decimalprice_local.find('1'))-1
        
        step_size = None
        for f in symbolinfo['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_size = f['stepSize']
                break
        roundqty = (step_size.find('1'))-1
        
        roundplace = (roundprice,roundqty)
        return roundplace
    
    def _trc(self,num,n):
        i = int(num * (10**n))/(10**n)
        return i
            
            
            
bot = botrack()
#bot.cancel_order(12959049604)
#bot.send_order('BUY','LIMIT',0.0073,1800)
#bot.update_time()
bot.get_rack_list()
#bot._regtrade()
#n = 0
while True:
    #n+=1
    time.sleep(1)
    bot.run()
