import matplotlib.pyplot as plt
import pandas as pd

prices = pd.read_csv('ETHUSDT4hour6monthn.csv')
prices.set_index('Date', inplace=True)
prices = prices.iloc[0:20,:]
#prices = pd.DataFrame({'Open': [data['Open']],
#                       'Close': [data['Close']],
#                       'High': [data['High']],
#                       'Low': [data['Low']]},
#                       index=pd.date_range("2021-01-01", periods=8, freq="d"))

#create figure
plt.figure()

#define width of candlestick elements
width = .4
width2 = .05

#define up and down prices
up = prices[prices.Close>=prices.Open]
down = prices[prices.Close<prices.Open]

#define colors to use
col1 = 'green'
col2 = 'red'

#plot up prices
plt.bar(up.index,up.Close-up.Open,width,bottom=up.Open,color=col1)
plt.bar(up.index,up.High-up.Close,width2,bottom=up.Close,color=col1)
plt.bar(up.index,up.Low-up.Open,width2,bottom=up.Open,color=col1)

#plot down prices
plt.bar(down.index,down.Close-down.Open,width,bottom=down.Open,color=col2)
plt.bar(down.index,down.High-down.Open,width2,bottom=down.Open,color=col2)
plt.bar(down.index,down.Low-down.Close,width2,bottom=down.Close,color=col2)

#rotate x-axis tick labels
plt.xticks(rotation=90, ha='right')

#display candlestick chart
plt.show()
