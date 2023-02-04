import config
from binance.client import Client
from binance.enums import *
import numpy as np

client = Client(config.API_KEY, config.API_SECRET, tld='com')

tickers = client.get_all_tickers()
maxPrecio = 0
maxMoneda = ''
minPrecio = 999999
minMoneda = ''


for tick in tickers:
    if tick['symbol'][-4:] != 'USDT':
        continue
    klines = np.array(client.get_historical_klines(tick['symbol'], Client.KLINE_INTERVAL_15MINUTE, "15 minute ago UTC")).astype(np.float64)
    if len(klines) != 1:
        continue

    variation = klines[0,4] * 100 /  klines[0,1]

    if maxPrecio < variation:
        maxPrecio = variation
        maxMoneda = tick['symbol']

    if minPrecio > variation:
        minPrecio = variation
        minMoneda = tick['symbol']

    print("MAYOR " , maxMoneda ,  " " , maxPrecio)
    print("MENOR " , minMoneda ,  " " , minPrecio)
    print("--------------------")