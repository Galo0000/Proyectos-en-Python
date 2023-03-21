import websocket
import json

# Función para procesar mensajes recibidos a través del WebSocket
def on_message(ws, message):
    data = json.loads(message)
    # Verificar si el mensaje es una actualización de balance
    if 'e' in data and data['e'] == 'balanceUpdate':
        # Imprimir el nuevo estado del balance
        print(f"Nuevo balance: {data['B'][0]['f']}")
    # Verificar si el mensaje es una actualización de precio
    if 'e' in data and data['e'] == 'kline' and data['s'] == 'ETHUSDT':
        # Imprimir el nuevo precio de Ethereum
        print(f"Nuevo precio de Ethereum: {data['k']['c']}")

# Función para manejar errores de conexión
def on_error(ws, error):
    print(error)

# Función para manejar el cierre de la conexión
def on_close(ws):
    print("Conexión cerrada.")

# Función para manejar la apertura de la conexión
def on_open(ws):
    print("Conexión abierta.")
    # Suscribirse a actualizaciones de balance
    ws.send(json.dumps({'method': 'SUBSCRIBE', 'params': ['balanceUpdate'], 'id': 1}))
    # Suscribirse a actualizaciones de precios de Ethereum
    ws.send(json.dumps({'method': 'SUBSCRIBE', 'params': ['ethusdt@kline_1m'], 'id': 2}))

# URL del WebSocket de Binance para recibir actualizaciones de balance y precios de Ethereum
websocket_url = 'wss://stream.binance.com:9443/ws'

# Crear una instancia del WebSocket
ws = websocket.WebSocketApp(websocket_url,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close,
                            on_open = on_open)

# Ejecutar el WebSocket en segundo plano
ws.run_forever()