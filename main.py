import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from helper import *

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

tickers_list = ["AAPL", "MSFT", "GOOG"]

def get_history(tickers_list):
    # This is part 1, data ingestion
    df_list = []
    for i in tickers_list:
        curr_ticker = yf.Ticker(i)
        df = curr_ticker.history(start="2020-01-01", end="2024-12-31", interval="1d", auto_adjust=True)
        df["Ticker"] = i
        df.set_index(["Ticker", df.index], inplace=True)
        df_list.append(df)

    final = pd.concat(df_list, axis=0)
    return final

def build_features(h_df):
    # This is part 2, feature engineering
    g = h_df.groupby(by="Ticker")

    merged_list = []
    for key, item in g:
        df = g.get_group(key)
        add_daily_return(df)
        add_moving_averages(df)
        add_rolling_volatility(df)
        merged_list.append(df)
    
    return pd.concat(merged_list)

def run_backtest(h_df):
    # This is part 3, backtesting
    g = h_df.groupby(by="Ticker")

    merged_list = []
    for key, item in g:
        df = g.get_group(key)
        add_strategy_return(df)
        add_strategy_cumulative_returns(df)
        add_BH_cumulative_returns(df)
        merged_list.append(df)
    
    return pd.concat(merged_list)

def report(h_df):
    # This is part 4, reporting
    g = h_df.groupby(by="Ticker")
    for key, item in g:
        df = g.get_group(key)
        print(get_evaluation_metrics(df))
    

    j = h_df.groupby(by="Ticker")

    fig, axes = plt.subplots(nrows=2, ncols=len(tickers_list))
    counter = 0

    for counter, (key, item) in enumerate(j):
        visualize_results(j.get_group(key), counter, axes)
    plt.subplots_adjust(hspace=0.5)
    fig.suptitle("Visualization of data")
    plt.show()


df = get_history(tickers_list)
df = build_features(df)
df = run_backtest(df)
report(df)

# my analysis on this project:
# If my short term moving averages eclipses the 
# long term moving average, then theres a signal in
# that row meaning we invest our money. This strategy
# did better for Google, but did not perform as well
# for Microsoft and Especially Apple. This is because
# during covid there was probably a recovery at 
# Apple and the 50 STMA to 200 LTMA wasn't fast enough
# to capture that. 


