import datetime
import websocket
import json
from common.database.market_data import MarketData
from services.db_crud_operations import bulk_create
from common.database.base import SessionLocal
db = SessionLocal()
import common.global_variables

SUPPORTED_SYMBOLS = ["btcusdt", "ethusdt", "ltcusdt"]
last_logged_times = {}
data_to_add = []

def on_message(ws_param, message):
    data = json.loads(message)
    current_price = float(data['c'])
    symbol = data['s']
    timestamp = datetime.datetime.now()
    if symbol not in last_logged_times:
        last_logged_times[symbol] = timestamp
    else:
        # log every 5 minutes
        if (datetime.datetime.now()- last_logged_times[symbol])<datetime.timedelta(minutes=5):
            return
    new_data = MarketData(timestamp, symbol, current_price)
    common.global_variables.current_symbol_prices[new_data.symbol] = {"price":new_data.price, "time":new_data.timestamp}
    data_to_add.append(new_data)
    if len(data_to_add)==12:
        bulk_create(db, MarketData, data_to_add)
        db.close()
        data_to_add.clear()


def on_error(ws_param, error):
    print(error)


def on_close(ws_param):
    print("WebSocket closed")


def on_open(ws_param):

    for symbol in SUPPORTED_SYMBOLS:
        ws_param.send(json.dumps({"method": "SUBSCRIBE", "params": [f"{symbol}@ticker"], "id": 1}))


# websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws", on_message=on_message, on_error = on_error, on_close = on_close)
ws.on_open = on_open
ws.run_forever()
