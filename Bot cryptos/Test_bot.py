
def _timesleep_():
    if generator:
        timepref = 0
    if not generator:
        timepref = 1.5
    time.sleep(timepref)

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
    
    
    if generator:
        klines = client.get_historical_klines(symbolTicker,Client.KLINE_INTERVAL_15MINUTE, '4 week ago')
        g = _generator_()
    rounds = _roundplaces_()
    balance = _balance_()
    indicadores = _indicators_()