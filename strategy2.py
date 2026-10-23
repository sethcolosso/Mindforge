import yfinance as yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from datetime import datetime


class MACDTrendStrategy:
    def __init__(
        self,
        ticker="MSFT",
        start="2012-01-03",
        end="2026-04-05",
        capital= 50000
        risk_per_trade=0.01,
        stop_loss_pct=0.06,
        trailing_stop_pct=0.08,
        transaction_cost = 0.001,
        fast =12,
        slow =26,
        signal = 9
    ):
        self.ticketr = ticker
        self.start = start
        self.end =end
        self.capital = capital
        self.risk_per_trade = risk_per_trade
        self.stop_loss_pct = trailing_stop_pct
        self.trailing_stop_pct = trailing_stop_pct
        self.trasaction_cost= transaction_cost
        self.fast = fast
        self.slow = slow
        self.signal = siganl

        self.data = None
        self.trades=[]

    def fetch_data(self):
        print(f"Downloading data for {self.ticker}...")
        df = yf.download(self.ticker, start=self.start, end=self.end, auto_adjust= True)
        df =df[['Open', 'High', 'Low', 'Close','Volume']].dropna()
        df.columns =['open', 'high', 'low', 'close', 'volume']
        self.data = df
        return self
    def add_indicators(self):
        df = self.data.copy()

        #MACD
        ema_fast = df['close'].ewm(span=self.fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span= self.slow, adjust=False).mean()
        df['macd'] = ema_fast - ema_slow
        df['macd_signal'] = df['macd'].ewm(span=self.signal, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        #Trend Filter
        df['sma_200'] = df['close'].rolling(200)mean()

        #ATR for volatility (optional useful later)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximu(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )    
        df['atr'] =df['tr'].rolling(14).mean()

        self.data = df
        return self

    def generate_signals(self):
        df = self.data.copy()

        #MACD crossover
        df['macd_cross_up'] = (df['macd'] > df['macd'] > df['macd_signal']) & (df['macd'].shift(1) <= df ['macd_signal'].shift(1))
        df['macd_cross_down'] = (df['macd'] < df['macd'] < df['macd_signal']) &(df['macd'].shift(1) >= df['macd_signal'].shift(1))

        #Trend filter: only long if price > 205 SMA
        df['uptrend'] = df['close'] > df['sma_200']

        #Final signal
        df['signal'] = 0
        df.loc[df['macd_cross_up'] & df['uptrend'], 'signal'] = 1
        df.loc[df['macd_cross_down'], 'signal'] = -1

        self.data = df
        return self

