
buy_price = 1850
current_price = 1900
quantity = 0.14830
fee = 0.001
usdt_profit = 0.5

usdt_profit = (current_price * quantity * (1 - fee)) - (buy_price * quantity * (1 + fee))



print("USDT Profit: ", usdt_profit)
print(buy_price * quantity * (1 + fee))