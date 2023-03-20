import sys

buy_price = 3000
current_price = 3600
quantity = 0.005
fee = 0.001

usdt_profit = (current_price * quantity * (1 - fee)) - (buy_price * quantity * (1 + fee))

print("USDT Profit: ", usdt_profit)

sys.path.append( 'C:/Repositorios/Python' )
import USERBINANCE
from binance.client import Client
basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin
client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET, tld='com')
symbolinfo = client.get_symbol_info(symbolTicker)
print(symbolinfo)