from binance.websocket import BinanceSocketManager
from binance.client import Client
import sys
sys.path.append( 'C:/Repositorios/Python' )
import USERBINANCE

# Creamos una instancia del cliente de Binance y nos autenticamos
client = Client(USERBINANCE.API_KEY, USERBINANCE.API_SECRET)

# Creamos una instancia del Socket Manager
socket_manager = BinanceSocketManager(client)

# Definimos una función de devolución de llamada para procesar las actualizaciones de precios
def process_price_message(msg):
    print(f"Precio de {msg['s']}: {msg['c']}")

# Definimos una función de devolución de llamada para procesar las actualizaciones de saldo
def process_balance_message(msg):
    print(f"Saldo de {msg['a']} en {msg['B']}: {msg['d']['w']} {msg['d']['a']}")

# Nos suscribimos a los canales de WebSocket para recibir actualizaciones de precios y cambios de saldo
price_socket = socket_manager.start_symbol_ticker_socket('BTCUSDT', process_price_message)
balance_socket = socket_manager.start_user_socket(process_balance_message)

# Iniciamos el Socket Manager
socket_manager.start()

# Mantenemos la ejecución del programa
while True:
    pass