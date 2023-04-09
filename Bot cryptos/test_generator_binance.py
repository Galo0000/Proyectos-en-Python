from binance.client import Client
import datetime
import sys
sys.path.append( 'C:/Repositorios/Python' )
import USERBINANCE

# Inserte aquí su API key y API secret
client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')

basecoin = 'USDT'
tradecoin = 'ETH'
symbol = tradecoin + basecoin
interval = "1d"
start_date = datetime.datetime(2022, 1, 1)
end_date = datetime.datetime(2022, 1, 31)
klines_generator = client.get_historical_klines_generator(symbol, interval, start_date, end_date)

# Imprimir los datos de precios históricos
print(next(klines_generator))