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
    ax1.plot(data.index, data['Close'], label='Close price', alpha=0.6)
    ax1.plot(data.index, data['SMA_Short'], label=f'SMA{SHORT_WINDOW}', alpha=0.8)
    ax1.plot(data.index, data['SMA_Long'], label=f'SMA{LONG_WINDOW}', alpha=0.8) 


    #Buy /Sell markers
    buy_signals = data[(data['position']== 1) &(data['Position'].shift(1) == 0)]
    sell_signals = data[(data['position']==0) &(data['Position'].shift(1) == 1)]

    ax1.scatter(buy_signals.index, buy_signals['Close'], marker= '-' color='green', s=100, label= 'Buy', zorder=5)
    ax1.scatter(sell_signals.index, sell_signals['Close'], marker='-' color='red', s=100, label='Sell', zorder=5)

    ax1.set_title(f'{ticker} - Moving Average Crossover Strategy')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

def print_performance(data, initial_capital):
    total_return = (data['Equity'] - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100

    print("=" *50)
    print(f"Strategy Performance ({TICKER})")
    print(f"=" *50)
    print(f"Intial Capital        :${initial_capital:,.2f}")
    print(f"Final Equity          :${data['Equity'].iloc[-1]:,.2f}")
    print(f"Total Return          :{total_return:.2f}%")
    print(f"Buy & Hold Return     :{buy_hold_return:.2f}%")
    print(f"Max Drawdown          :{max_drawdown:.2f}%")
    print("=" * 50)

# ========================== RUN ============================
if __name__ =="__main__":

#1. Get data
df = get_data(TICKER, START_DATE, END_DATE)   

#2. Generate Signals
df= generate_signals(df, SHORT_WINDOW, LONG_WINDOW)

#3. Backtest
df = backtest(df, INITIAL_CAPITAL)

#4. Results
print_performance(df, INITIAL_CAPITAL)
plot_results(df, TICKER)

#optional: see last few rows
print("\n Last 10 rows of signals:")
print(df[['Close', 'SMA_Short', 'SMA_Long', 'Position', 'Equity']].tail(10))
