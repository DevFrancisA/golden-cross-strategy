import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def add_daily_return(h_df):
    s = h_df["Close"]
    s_shifted = s.shift(periods=1)
    h_df["Daily Return"] = (s - s_shifted) / s_shifted


def add_moving_averages(h_df):
    h = h_df["Close"]
    h_df["STMA"] = (h.rolling(50).sum())/50
    h_df["LTMA"] = (h.rolling(200).sum())/200

def get_single_volatility(h_df):
    d = h_df["Daily Return"]
    return d.std()

def add_rolling_volatility(h_df):
    d = h_df["Daily Return"]
    h_df["Rolling Volatility"] = d.rolling(10).std()

def add_strategy_return(h_df):
    # signal
    h_df["Signal"] = np.where(h_df["STMA"] > h_df["LTMA"], 1, 0)

    # strategy return
    h_df["Strategy Return"] = h_df["Daily Return"] * h_df["Signal"].shift(periods=1)

def add_strategy_cumulative_returns(h_df):
    # strategy cumulative return
    sr = h_df["Strategy Return"]
    h_df["Strategy Cumulative Return"] = np.cumprod(sr + 1)

def add_BH_cumulative_returns(h_df):
    # buy and hold cumulative return
    dr = h_df["Daily Return"]
    h_df["BH Cumulative Return"] = np.cumprod(dr + 1)

def get_evaluation_metrics(h_df):
    T = h_df.index.get_level_values(0)[0]
    BH = h_df["Daily Return"]
    S = h_df["Strategy Return"]
    BH_C = h_df["BH Cumulative Return"]
    S_C = h_df["Strategy Cumulative Return"]
    SI = h_df["Signal"]
    BH_total_return = float(BH_C.iloc[-1] - 1)
    S_total_return = float(S_C.iloc[-1] - 1)
    BH_volatility = float(BH.std())
    S_volatility = float(S.std())
    days_in_market = (SI == 1).sum()

    return f"""{T}:
    BH_total_return: {BH_total_return}, 
    S_total_return: {S_total_return}, 
    BH_volatility: {BH_volatility}, 
    S_volatility: {S_volatility}, 
    Days In Market: {days_in_market}"""

def visualize_results(h_df, counter, axes):

    T = h_df.index.get_level_values(0)[0]
    strat_cum = h_df["Strategy Cumulative Return"]
    BH_cum = h_df["BH Cumulative Return"]
    short_MA = h_df["STMA"]
    long_MA = h_df["LTMA"]
    dates = h_df.index.get_level_values("Date")
    close = h_df["Close"]


    axes[0,counter].plot(dates, close, label = "close")
    axes[0,counter].plot(dates, short_MA, label = "short MA")
    axes[0,counter].plot(dates, long_MA, label = "long MA")

    axes[0,counter].set_xlabel("Date")
    axes[0,counter].set_ylabel("Price")
    axes[0,counter].set_title(f"{T} Time vs short MA,\n long MA, Close")
    axes[0,counter].legend()

    axes[1,counter].plot(dates, strat_cum, label = "Strategy Cumulative Return")
    axes[1,counter].plot(dates, BH_cum, label = "BH Cumulative Return")

    axes[1,counter].set_xlabel("Date")
    axes[1,counter].set_ylabel("Cumulative Return")
    axes[1,counter].set_title(f"{T} Time vs Strategy \nand BH Cumulative Returns")
    axes[1,counter].legend()
    
    










