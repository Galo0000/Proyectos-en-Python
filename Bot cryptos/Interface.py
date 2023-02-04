import tkinter as tk
from random import randrange

######################################## VENTANA TKINTER ###################################
window = tk.Tk()
window.geometry('300x600')
#window.configure(background='black')
window.title("Terminator Bot")

def update():
    lblinfo_price.config(text=randrange(1000))
    lblinfo_price.after(1000, update)

lbl_symbolTicker = tk.Label(window,text = 'str(symbolTicker').grid(row = 0, column = 0)

lbl_date = tk.Label(window,text = 'indicadores[''closetime'']')
lbl_date.grid(row = 1, column = 0)

#if status == 'zc':
#        x = 'ZONA DE COMPRA'
#elif status == 'zv':
#        x = 'ZONA DE VENTA'
#elif status == 'cd':
#        x = 'COMPRA DINAMICA'
#elif status == 'vd':
#        x = 'VENTA DINAMICA'
lbl_status = tk.Label(window,text = 'x')

lbl_trend = tk.Label(window,text = 'Tendencia     = ')
lbl_EMA4 = tk.Label(window,text =  'EMA 4         = ')
lbl_EMA9 = tk.Label(window,text =  'EMA 9         = ')
lbl_EMA18 = tk.Label(window,text = 'EMA 18        = ')
lbl_price = tk.Label(window,text = 'Precio actual = ')

lblinfo_trend = tk.Label(window,text = 'indicadores[''tendencia'']')
lblinfo_EMA4 = tk.Label(window,text = 'indicadores[''EMA4'']')
lblinfo_EMA9 = tk.Label(window,text = 'indicadores[''EMA9'']')
lblinfo_EMA18 = tk.Label(window,text = 'indicadores[''EMA18'']')
lblinfo_price = tk.Label(window,text = '')
update()




lbl_trend.grid(row = 2, column = 0)
lbl_EMA4.grid(row = 3, column = 0)
lbl_EMA9.grid(row = 4, column = 0)
lbl_EMA18.grid(row = 5, column = 0)
lbl_price.grid(row = 6, column = 0)

lblinfo_trend.grid(row = 2, column = 1)
lblinfo_EMA4.grid(row = 3, column = 1)
lblinfo_EMA9.grid(row = 4, column = 1)
lblinfo_EMA18.grid(row = 5, column = 1)
lblinfo_price.grid(row = 6, column = 1)

#if status == 'cd' or status == 'vd':
#    lbl_prevprice = tkinter.Label(window,text = " Precio previo          = ")
#    lbl_paux = tkinter.Label(window,text =      " Precio seteado actual  = ")
#    lbl_quantity = tkinter.Label(window,text =  " Cantidad               = ")

#    lblinfo_prevprice = tkinter.Label(window,text = prev_symbolPrice)
#    lblinfo_paux = tkinter.Label(window,text = round(paux,2))
#    lblinfo_quantity = tkinter.Label(window,text = quantity)

#    lbl_prevprice.grid(row = 6, column = 0)
#    lbl_paux.grid     (row = 7, column = 0)
#    lbl_quantity.grid (row = 8, column = 0)

#    lblinfo_prevprice.grid(row = 6, column = 1)
#    lblinfo_paux.grid     (row = 7, column = 1)
#    lblinfo_quantity.grid (row = 8, column = 1)

#if status == 'vd':
#    lbl_buyprice = tkinter.Label(window,text = " Precio de compra        = ")
#    lblinfo_buyprice = tkinter.Label(window,text = round(pstatus,2))

#    lbl_buyprice.grid(row = 9, column = 0)
#    lblinfo_buyprice (row = 9, column = 1)
#if status == 'zc' or status == 'zv':

#    lbl_RSI = tkinter.Label(window,text =      " RSI actual              = ")
#    lbl_RSIlimit = tkinter.Label(window,text = " limite RSI              = ")

#    lblinfo_RSI = tkinter.Label(window,text = indicadores['RSI'])
#    lblinfo_RSIlimit = tkinter.Label(window,text = rsiconf)

#    lbl_RSI.grid    (row = 9, column = 0)
#    lblinfo_RSIlimit(row = 9, column = 0)

#    lblinfo_RSI.grid(row = 9, column = 1)
#    lblinfo_RSIlimit(row = 9, column = 1)


#print("*******************************")
#if status == 'zv':
#    print(" Margen                  = " + str(round((quantity*indicadores['closeprice']) - coinbaseini,4)))
#if status == 'vd':
#    if ((quantity*paux) - coinbaseini) > 0:
#        print(" Ganancia actual         = " +Fore.GREEN+str(round((quantity*paux) - coinbaseini,4))+Style.RESET_ALL)
#    else:
#        print(" Ganancia actual         = " +Fore.RED+str(round((quantity*paux) - coinbaseini,4))+Style.RESET_ALL)
#    
#print(" Ganancia Total          = " + str(round(profit,2)))
#print("********************************")
#print(" USDT total              = " + str(balance['coinbase']))
#print(" BNB total               = " + str(balance['cointrade']))
#print("********* registro de trades **********")
#print(regprofit)

window.mainloop()

















