import os.path
import pandas as pd


class Tools:
    def __init__(self):
        self.tol = 0.5
        self.paux = 0
        self.maxtimes = 12
        self.times = self.maxtimes
        if tradecoin == 'BNB':
            self.fees = 0.99925
        else:
            self.fees = 0.999 
    
    def _truncate_(self,num,dec):
        integer = int(num * (10**dec))/(10**dec)
        return float(integer)
    
    def _valuebuy_(self,value,tol):
        result = 0
        
        if value == 'lstid':
            templst = []
            for a in range(0,len(regbuys)):
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
            for a in range(0,len(regbuys)):
                result += regbuys.iloc[a]['qty']
        elif value == 'invini':
            for t in range(0,len(regbuys)): 
                if regbuys.iloc[t]['ganancia'] > tol:
                    result += regbuys.iloc[t]['inversion']
        return result
    
    def update_regs(self):
        global regbuys
            
        for a in range(0,len(regbuys)):
            try:
                regbuys.at[a,'ganancia'] = self._truncate_((((regbuys.iloc[a]['qty']*paux)*self.fees)-regbuys.iloc[a]['inversion']),4)
            except ValueError:
                pass
    
            
    def _acta_(self,date,location,action):
        if not os.path.isfile('acta.csv'):
            df = pd.DataFrame(columns=['date','location','action'])
            df.set_index('date', inplace=True)
            df.to_csv('acta.csv')
        temp = pd.read_csv('acta.csv')
        temp = pd.DataFrame({'date': [date],'location': [location],'action': [action]})
        temp.to_csv('acta.csv',index = False, header = False, mode = 'a')
        
        
        
    def _buyslist_(self,addordelete,idbuy,date,buyp,qty,inv):
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
            times = self.maxtimes - len(regbuys)
        if addordelete == 'delete':
            temp = pd.read_csv(file)
            for a in range(0,len(idbuy)):
                try:
                    temp = temp.drop(temp[(temp['id']==idbuy[a])].index)
                    regbuys = regbuys.drop(regbuys[(regbuys['id']==idbuy[a])].index)
                except IndexError:
                    pass
                        
            temp.to_csv(file,index = False)
            times = self.maxtimes - len(regbuys)
            
    
    def _regtrades_(self,date,bprice,sprice,profit,balance,qty,basecoin,tradecoin):
        global regprofit
        
        if not os.path.isfile('regtrades.xlsx'):
            df = pd.DataFrame(columns=['Fecha y Hora','Compra','Venta','Ganancia','Balance','Cantidad','Moneda base','Moneda cambio'])
            df.to_excel('regtrades.xlsx',sheet_name='regtrades', index=False)
            
        tempregprofit = pd.DataFrame({'Fecha y Hora': [date]
                                    ,'Compra': [bprice]
                                    ,'Venta': [sprice]
                                    ,'Ganancia':[profit]
                                    ,'Balance':[balance]
                                    ,'Cantidad':[qty]
                                    ,'Moneda base':[basecoin]
                                    ,'Moneda cambio':[tradecoin]
                                    })
        regprofit = regprofit.append(tempregprofit,ignore_index = True)
        regprofit.to_excel('regtrades.xlsx', sheet_name='regtrades', index=False)
        
        
        
    def _quantity_(self):
        quantity = 0
        if self.inversion == 0 and status == 'cd':
            tempqty = (int(self.balance['basecoin'])/times)/paux
            quantity = _truncate_(tempqty,rounds['roundqty'])

        if self.inversion == 0 and status == 'vd':
            tempq = 0
            for t in range(0,len(regbuys)): 
                if regbuys.iloc[t]['ganancia'] > self.tol:
                    tempq += regbuys.iloc[t]['qty']
            if tempq == 0:
                tempdfmin = _valuebuy_('min')
                tempq = tempdfmin.iloc[0]['qty']
                        
            quantity = _truncate_(tempq,rounds['roundqty'])
        return quantity
    
    
    def _nextbuy_(self):
        global paux,prev_symbolPrice,status,quantity
        status = 'cd'
        indicadores = _indicators_()
        paux = _truncate_((indicadores['closeprice'] * ppbuy),rounds['roundprice'])
        while 1:
            scr.clear()
            indicadores = _indicators_()
            update_regs()
            quantity = _quantity_()
            _interface_()

            if indicadores['closeprice'] > paux:
                break
            if indicadores['closeprice'] < prev_symbolPrice:
                paux = _truncate_((indicadores['closeprice'] * ppbuy),rounds['roundprice'])
                prev_symbolPrice = indicadores['closeprice']
                _timesleep_()
                continue
            else:
                _timesleep_()
                continue
                
        order_inputdata = {'type':'buy'
                           ,'pair':symbolTicker
                           ,'paux':paux
                           ,'qty':quantity}
        _order_(order_inputdata)
        _timesleep_()
        
        
        
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
            scr.addstr(row,0,' BB up   = '+str(round(indicadores['BBANDS-upper'],rounds['roundprice'])))
            row += 1
            scr.addstr(row,0,' BB mid  = '+str(round(indicadores['BBANDS-middle'],rounds['roundprice'])))
            row += 1
            scr.addstr(row,0,' BB down = '+str(round(indicadores['BBANDS-lower'],rounds['roundprice'])))
            row += 1
            scr.addstr(row,0,' STOCHRSI K = '+str(round(indicadores['STOCHRSI_fastk'],2)))
            row += 1
            scr.addstr(row,0,' STOCHRSI D = '+str(round(indicadores['STOCHRSI_fastd'],2)))
            row += 1
            scr.addstr(row,0,' ADX = '+str(round(indicadores['ADX'],2)))
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
            scr.addstr(row,0," Precio actual           = " + str(indicadores['closeprice']))
            row += 1
            if status == 'cd' or status == 'vd':
                scr.addstr(row,0," Precio seteado actual   = " + str(round(paux,rounds['roundprice'])))
                row += 1
            scr.addstr(row,0," Precio tope de recompra   = " + str(round(tempzone,rounds['roundprice'])))
            row += 1
            scr.addstr(row,0,"*******************************")
            row += 1
            if status == 'z':
                scr.addstr(row,0,"Esperando ")
                row += 1
            scr.addstr(row,0," Ganancia Total          = " + str(round(profit,8)))
            row += 1
            scr.addstr(row,0,"********************************")
            row += 1
            scr.addstr(row,0,str(basecoin) +  " total               = " + str(f"{balance['basecoin']:.8f}"))
            row += 1
            scr.addstr(row,0,str(tradecoin) + " total                = " + str(f"{balance['tradecoin']:.8f}"))
            row += 1
            scr.addstr(row,0,"********* registro de trades **********")
            row += 1
            try:
                scr.addstr(row,0,str(regprofit))
            except curses.error:
                pass
            scr.refresh()