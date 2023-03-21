
buy_price = 1616.76
current_price = 1738
quantity = 0.0073
fee = 0.001

usdt_profit = (current_price * quantity * (1 - fee)) - (buy_price * quantity * (1 + fee))

print("USDT Profit: ", usdt_profit)