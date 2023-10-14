import sys
import userbinance
import matplotlib.pyplot as plt
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
from binance.client import Client
import numpy as np
from matplotlib.animation import FuncAnimation

# Initialize Binance client
client = Client(userbinance.API_KEY, userbinance.API_SECRET, tld='com')

# Parameters
nl = 100
basecoin = 'USDT'
tradecoin = 'ETH'
symbolTicker = tradecoin + basecoin
interval = Client.KLINE_INTERVAL_4HOUR

# Function to fetch data and process
def fetch_and_process_data():
    klines = np.array(client.get_klines(symbol=symbolTicker, interval=interval, limit=nl)).astype(np.float64)
    df = pd.DataFrame(klines[:, :5], columns=['Date', 'Open', 'High', 'Low', 'Close'])
    df['Date'] = np.round(df['Date'], 5)
    return df


# Function to update the plot
def update_plot(i):
    df = fetch_and_process_data()

    x = [df['Date'].iloc[0], df['Date'].iloc[-1]]
    xcord = df['Date'].iloc[0]

    # Clear previous plot
    ax.clear()

    # Plot the new data
    candlestick_ohlc(ax, df.values, width=10000000, colorup='green', colordown='red')

    ax.set_title('ETHUSDT')

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(32, 24))

# Set up the animation
ani = FuncAnimation(fig, update_plot, interval=1000)  # Update every 10 seconds (10000 milliseconds)

plt.show()
