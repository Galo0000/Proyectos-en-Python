
buy_price = 1616.76
current_price = 1740
quantity = 0.01
fee = 0.0073
usdt_profit = 0.5

usdt_profit = (current_price * quantity * (1 - fee)) - (buy_price * quantity * (1 + fee))



print("USDT Profit: ", usdt_profit)