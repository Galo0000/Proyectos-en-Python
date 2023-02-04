from websocket import WebSocketApp
import json
import numpy

def on_message(ws, msg):
    tick = json.loads(msg)
    a = float(tick['k']['c'])
    print(numpy.round_(a,decimals = 2, out = None))


ws = WebSocketApp("wss://stream.binance.com:9443/ws/ethusdt@kline_1m", on_message=on_message)
ws.run_forever()