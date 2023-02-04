import pandas as pd
import os.path

df = None

if not os.path.isfile("testbuylist.csv"):
    df = pd.DataFrame({'id':pd.Series([],dtype='int')
                           ,'buyp':pd.Series([],dtype='float64')
                           ,'qty':pd.Series([],dtype='float64')
                           ,'date':pd.Series([],dtype='str')})
    df.set_index('id', inplace=True)
    df.to_csv('testbuylist.csv')
    print('el archivo no existe, creando...')
    
def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)


a1 = 3000
a2 = 0.009
b1 = 2500
b2 = 0.08
c1 = 2800
c2 = 0.0081
d1 = 3500
d2 = 0.0091

#tempminbuylst = temp[temp['buyp']==temp['buyp'].min()]
#result = tempminbuylst['qty'] * float(tempminbuylst['buyp'])

def _buyslist_(addordelete,idbuy,buyp,qty,profit):
    global df
    if addordelete == 'add':
        #temp = pd.read_csv('testbuylist.csv')
        df = pd.DataFrame({'id': [idbuy],'buyp': [buyp],'qty': [qty],'profit':[None]})
        df.to_csv('testbuylist.csv',index = False, header = False, mode = 'a')
    if addordelete == 'delete':
        temp = pd.read_csv('testbuylist.csv')
        temp = temp.drop(temp[(temp['id']==idbuy)].index)
        temp.to_csv('testbuylist.csv',index = False)

#_buyslist_('add',223,a1, a2,None)
#_buyslist_('add',224,b1, b2,None)
#_buyslist_('add',225,c1, c2,None)
#_buyslist_('add',226,d1, d2,None)
#_buyslist_('delete',224,b1, b2,None)


#temp = pd.read_csv('testbuylist.csv')
#for a in range(0,len(temp)):
#    print(str(a))
#    print(str(temp.iloc[a]['buyp']))
    #print(temp[a:0])
    
    
    
#for a in range(0,len(temp)):
#		temp.at[a,'profit'] = float(temp.iloc[a]['qty'])*float(temp.iloc[a]['buyp'])
#_buyslist_('add',227,3338, 0.0400,None)

#for a in range(0,len(temp)):
#		temp.at[a,'profit'] = float(temp.iloc[a]['qty'])*float(temp.iloc[a]['buyp'])
#print('calculo y muestreo de valor de fila calculada')
#print(temp)
#print('******************************************************')
#print('numero de filas')
#print(len(temp))
#print('******************************************************')
#print('fila de valor maximo')
#print(temp[temp['buyp']==temp['buyp'].max()])
#print('******************************************************')
#print('Valor maximo de compra')
#tempmax = temp[temp['buyp']==temp['buyp'].max()]
#print(float(tempmax['buyp']))
#print('******************************************************')
#print('Valor minimo de compra')
#tempmin = temp[temp['buyp']==temp['buyp'].min()]
#print(tempmin.iloc[0]['buyp'])
#print(tempmin.iloc[0]['qty'])
#print('******************************************************')
#print('truncado de 0,08999 a 0,0899')
#print(str(truncate(0.08999,4)))
#print('limpio')
#temp = temp.iloc[0:0]
#print(temp)
#print('******************************************************')#

time = str(pd.to_datetime(int(1499865549590),unit='ms'))
time = time[:time.rfind(".")]
print(time)

