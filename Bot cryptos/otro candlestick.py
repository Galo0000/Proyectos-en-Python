import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates

prices = pd.read_csv('ETHUSDT4hour6monthn.csv')
prices.set_index('Date', inplace=True)
prices = prices.iloc[0:20,:]

plt.style.use('ggplot')

# Creating Subplots
fig, ax = plt.subplots()

candlestick_ohlc(ax, prices.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

# Setting labels & titles
ax.set_xlabel('Date')
ax.set_ylabel('Price')
fig.suptitle('Daily Candlestick Chart of NIFTY50')

# Formatting Date
date_format = mpl_dates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

fig.tight_layout()

plt.show()