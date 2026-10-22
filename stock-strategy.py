 import yfinance as yf
 import pandas as pd
 import numpy as np
 import matplotlib.pypyplot as plt

 #==========================CONFIG==================================================
 TICKER ="MSFT"
 END_DATE= "2026-05-03"
 START_DATE ="2015-07-07"
 LONG_WINDOW = 50
 SHORT_WINDOW = 20
 INITIAL _CAPITAL= 50000
 #=====================================================================================


 def get_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end, auto_adjust =True)
    data = data[['Close']].copy()
    data.columns = ['Close']
    return data

def generate_signals(data, short_window, long_window):
    data = data.copy()

    # Calculate moving averages
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()

    # Generate signals
    data['Signal'] = 0
    data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] =1
    data.loc[data['SMA_Short'] < data['SMA_Long'], 'Signal'] =0

    # position: 1=long, 0 =cash
    data['Position'] = data['Signal'].shift(1)
    data['Position'] = data['Position'].fillna(0)

    return data

def backtest(data, initial_capital=50000):
    data = data.copy()

    # Daily returns of the asset
    data['Returns'] = data['Close'].pct_change()

    # Strategy returns (only when we are long)
    data['Strategy_Returns'] = data['Position'] * data['Returns']

    # Equity Curve
    data['Equity'] = (1 + data['Strategy_Returns']).cumprod() * initial_capital
    data['Buy_Hold_Equity'] = (1 + data['Returns']).cumprod() * initial_capital

    return data

def plot_results(data, ticker):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize =(14, 10), gridspec_kw={'height_ratios': [2, 1]}) 

    #Price + Moving Averages
       