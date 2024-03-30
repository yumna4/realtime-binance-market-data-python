import datetime
current_symbol_prices = {"BTCUSDT": {"time":datetime.datetime(2024, 3, 30, 0, 0, 0), "price": 0.0},
                         "ETHUSDT": {"time":datetime.datetime(2024, 3, 30, 0, 0, 0),"price": 0.0},
                         "LTCUSDT": {"time":datetime.datetime(2024, 3, 30, 0, 0, 0), "price": 0.0}}


def update_current_prices(new_data):
    current_symbol_prices[new_data.symbol] = {"price":new_data.price, "time":new_data.timestamp}
